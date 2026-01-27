import base64
import csv
import logging
import os
import re
from contextlib import suppress
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd

from PyQt6.QtCore import (
    QSize,
    Qt,
    QTimer,
)
from PyQt6.QtGui import QColor
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
    QSizePolicy,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from src.core.constants import Icons
from src.core.database import db_manager
from src.core.report_history import ReportHistory
from src.gui.formatters import FastTableModel
from src.gui.panels.dipendenti.shared import (
    ColoredDotDelegate,
    InteractiveStatusCard,
    create_field_row,
    create_info_card,
)
from src.gui.widgets.toast import ToastManager
from src.utils.helpers import get_asset_path, get_colored_icon

logger = logging.getLogger(__name__)


class AnagraficaPage(QWidget):
    """Pagina per la visualizzazione e gestione anagrafica dipendenti."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.master_headers = [
            "SCAD.\nISAB",
            "ID\nRISORSA",
            "Cognome",
            "Nome",
            "CODICE FISCALE",
            "ID\nBADGE",
            "DATA\nASSUNZIONE",
        ]

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
        self.current_filter = None

        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.refresh_data)

        self._setup_ui()
        QTimer.singleShot(50, self.refresh_data)

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # 1. Filtri e Azioni
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

        email_report_btn = QPushButton("Genera Report via Email")
        email_report_btn.setIcon(
            get_colored_icon(get_asset_path(Icons.SEND), "#ffffff")
        )
        email_report_btn.setIconSize(QSize(24, 24))
        email_report_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #0d6efd;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 15px;
                font-weight: 600;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #0b5ed7;
            }
            QPushButton:pressed {
                background-color: #0a58ca;
            }
        """
        )
        email_report_btn.clicked.connect(self._generate_email_report)
        filter_layout.addWidget(email_report_btn)

        main_layout.addLayout(filter_layout)

        # Cards Container
        self.cards_container = QWidget()
        cards_layout = QHBoxLayout(self.cards_container)
        cards_layout.setContentsMargins(0, 5, 0, 5)
        cards_layout.setSpacing(15)

        self.card_ok = InteractiveStatusCard(
            "Operativi", "#198754", Icons.CHECK_CIRCLE, "Ultimo accesso ≤20gg", "ok"
        )
        self.card_warning = InteractiveStatusCard(
            "In Scadenza",
            "#fd7e14",
            Icons.ALERT_TRIANGLE,
            "Accesso 21-30gg fa",
            "warning",
        )
        self.card_expired = InteractiveStatusCard(
            "Scaduti", "#dc3545", Icons.X_CIRCLE, "Accesso >30gg fa", "expired"
        )
        self.card_excluded = InteractiveStatusCard(
            "Esclusi",
            "#6c757d",
            Icons.EYE_OFF,
            "Non monitorati",
            "excluded",
        )

        self.card_ok.clicked.connect(self._on_card_filter)
        self.card_warning.clicked.connect(self._on_card_filter)
        self.card_expired.clicked.connect(self._on_card_filter)
        self.card_excluded.clicked.connect(self._on_card_filter)

        cards_layout.addWidget(self.card_ok, stretch=1)
        cards_layout.addWidget(self.card_warning, stretch=1)
        cards_layout.addWidget(self.card_expired, stretch=1)
        cards_layout.addWidget(self.card_excluded, stretch=1)

        main_layout.addWidget(self.cards_container)

        # 2. Area Contenuti
        self.content_layout = QHBoxLayout()
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(10)

        # Tabella
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

        # Menu contestuale per bypass monitoraggio
        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self._show_context_menu)

        header = self.table.horizontalHeader()
        self.table.selectionModel().selectionChanged.connect(self._on_selection_changed)
        self.table.setItemDelegateForColumn(0, ColoredDotDelegate(self.table))

        # Larghezze colonne aumentate per evitare troncamenti
        self.column_widths = [80, 100, 200, 150, 180, 100, 145]
        for col_idx in range(len(self.column_widths)):
            header.setSectionResizeMode(col_idx, QHeaderView.ResizeMode.Fixed)
            self.table.setColumnWidth(col_idx, self.column_widths[col_idx])

        total_width = sum(self.column_widths) + 20
        self.table.setFixedWidth(total_width)

        # Imposta la larghezza delle card uguale a quella della tabella
        self.cards_container.setFixedWidth(total_width)

        self.content_layout.addWidget(self.table)

        # Pannello Destra (Scheda)
        self._setup_detail_view()
        main_layout.addLayout(self.content_layout)

    def _setup_detail_view(self):
        right_container = QWidget()
        right_container.setFixedWidth(360)
        right_container.setStyleSheet("QWidget { background-color: #f8f9fa; }")
        right_layout = QVBoxLayout(right_container)
        right_layout.setContentsMargins(10, 10, 10, 10)
        right_layout.setSpacing(8)  # Ridotto da 12 a 8

        header_card = QFrame()
        header_card.setFixedHeight(70)  # Ridotto da 80 a 70
        header_shadow = QGraphicsDropShadowEffect()
        header_shadow.setBlurRadius(20)
        header_shadow.setYOffset(3)
        header_shadow.setColor(QColor(0, 0, 0, 60))
        header_card.setGraphicsEffect(header_shadow)
        header_card.setStyleSheet(
            """
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #2196F3, stop:1 #1976D2);
                border-radius: 12px;
            }
        """
        )
        header_layout = QVBoxLayout(header_card)
        header_layout.setContentsMargins(18, 12, 18, 12)  # Ridotto per compattezza

        title_label = QLabel("📋 SCHEDA DIPENDENTE")
        title_label.setStyleSheet(
            "font-size: 20px; font-weight: bold; color: white; letter-spacing: 1px;"
        )
        subtitle_label = QLabel("Dettagli anagrafica e accessi")
        subtitle_label.setStyleSheet(
            "font-size: 14px; color: rgba(255, 255, 255, 0.90); margin-top: 2px;"
        )
        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle_label)
        right_layout.addWidget(header_card)

        # Content diretto senza scroll
        detail_content = QWidget()
        detail_content.setStyleSheet("background-color: transparent;")
        detail_layout = QVBoxLayout(detail_content)
        detail_layout.setContentsMargins(0, 0, 0, 0)
        detail_layout.setSpacing(8)  # Ridotto da 10 a 8 per compattezza

        personal_card, personal_layout = create_info_card("👤 Dati Personali")
        self.detail_labels = {}

        row1 = QHBoxLayout()
        row1.setSpacing(10)
        row1.addWidget(self._add_detail_field("ID Risorsa"))
        row1.addWidget(self._add_detail_field("Data Nascita"))
        personal_layout.addLayout(row1)

        row2 = QHBoxLayout()
        row2.setSpacing(10)
        row2.addWidget(self._add_detail_field("Cognome"))
        row2.addWidget(self._add_detail_field("Nome"))
        personal_layout.addLayout(row2)

        personal_layout.addWidget(self._add_detail_field("Codice Fiscale"))
        detail_layout.addWidget(personal_card)

        work_card, work_layout = create_info_card("💼 Informazioni Lavorative")
        row3 = QHBoxLayout()
        row3.setSpacing(10)
        row3.addWidget(self._add_detail_field("Badge"))
        row3.addWidget(self._add_detail_field("Data Assunzione"))
        work_layout.addLayout(row3)
        work_layout.addWidget(self._add_detail_field("Importato il"))
        detail_layout.addWidget(work_card)

        access_card = QFrame()
        access_shadow = QGraphicsDropShadowEffect()
        access_shadow.setBlurRadius(15)
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
        access_layout.setContentsMargins(15, 12, 15, 12)  # Ridotto per compattezza
        access_layout.setSpacing(6)  # Ridotto da 10 a 6

        access_title = QLabel("🏭 ULTIMO ACCESSO ISAB")
        access_title.setStyleSheet(
            "font-size: 13px; font-weight: bold; color: #2196F3; letter-spacing: 0.5px;"
        )
        self.last_access_label = QLabel("-")
        self.last_access_label.setWordWrap(True)
        self.last_access_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        self.last_access_label.setStyleSheet(
            "font-size: 16px; font-weight: bold; color: #2c3e50; padding: 5px 0;"
        )
        access_layout.addWidget(access_title)
        access_layout.addWidget(self.last_access_label)
        detail_layout.addWidget(access_card)

        detail_layout.addStretch()
        right_layout.addWidget(detail_content)

        self.content_layout.addWidget(right_container)
        self.content_layout.addStretch()

    def _add_detail_field(self, label):
        container = create_field_row(label)
        # Find the value label using objectName set in shared.py
        value_lbl = container.findChild(QLabel, "value_label")
        # Store tuple (container, value_label) or just value_label if that's what we update
        self.detail_labels[label] = value_lbl
        return container

    def _show_context_menu(self, position):
        """Mostra menu contestuale per gestione monitoraggio dipendente."""
        indexes = self.table.selectionModel().selectedRows()
        if not indexes:
            return

        row_idx = indexes[0].row()
        row_data = self.model._data[row_idx]
        id_risorsa = row_data[1]  # ID Risorsa

        # Verifica stato monitoraggio corrente
        query = "SELECT monitoraggio_attivo FROM dipendenti WHERE id_risorsa = ?"
        result = db_manager.execute_query(
            db_manager.DB_DIPENDENTI, query, (id_risorsa,)
        )
        is_monitored = result[0][0] if result and result[0][0] is not None else 1

        from PyQt6.QtGui import QAction
        from PyQt6.QtWidgets import QMenu

        menu = QMenu(self)

        if is_monitored:
            action = QAction(
                get_colored_icon(get_asset_path(Icons.X_CIRCLE), "#dc3545"),
                "🚫 Escludi da monitoraggio",
                self,
            )
            action.triggered.connect(lambda: self._toggle_monitoring(id_risorsa, False))
        else:
            action = QAction(
                get_colored_icon(get_asset_path(Icons.CHECK_CIRCLE), "#198754"),
                "✅ Riattiva monitoraggio",
                self,
            )
            action.triggered.connect(lambda: self._toggle_monitoring(id_risorsa, True))

        menu.addAction(action)
        menu.exec(self.table.viewport().mapToGlobal(position))

    def _toggle_monitoring(self, id_risorsa, enable):
        """Attiva o disattiva il monitoraggio per un dipendente."""
        try:
            query = "UPDATE dipendenti SET monitoraggio_attivo = ? WHERE id_risorsa = ?"
            db_manager.execute_query(
                db_manager.DB_DIPENDENTI, query, (1 if enable else 0, id_risorsa)
            )

            status_text = "riattivato" if enable else "escluso"
            ToastManager.instance().show(
                f"Monitoraggio {status_text} per il dipendente",
                "success",
                duration=2500,
            )
            self.refresh_data()
        except Exception as e:
            logger.error(f"Errore toggle monitoraggio: {e}")
            QMessageBox.critical(
                self, "Errore", f"Impossibile modificare il monitoraggio:\n{e}"
            )

    def refresh_data(self):
        search_text = self.search_input.text().lower()
        query = """
            SELECT id_risorsa, cognome, nome, data_nascita, badge, data_assunzione, created_at, codice_fiscale, monitoraggio_attivo
            FROM dipendenti WHERE 1=1
        """
        params = []
        if search_text:
            query += " AND (cognome LIKE ? OR nome LIKE ? OR badge LIKE ? OR codice_fiscale LIKE ?)"
            p = f"%{search_text}%"
            params.extend([p, p, p, p])
        query += " ORDER BY cognome ASC, nome ASC"

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

    def _process_employee_rows(self, full_rows):
        query_timb = "SELECT cognome, nome, codice_fiscale, data FROM timbrature"
        accessi = db_manager.execute_query(db_manager.DB_TIMBRATURE, query_timb)
        last_by_cf, last_by_name, normalize = self._build_timbrature_maps(accessi)

        master_rows = []
        count_ok = 0
        count_warning = 0
        count_expired = 0
        count_excluded = 0

        for r in full_rows:
            # r contiene ora anche monitoraggio_attivo come ultimo elemento
            is_monitored = r[8] if len(r) > 8 and r[8] is not None else 1

            (
                diff_days,
                cf_warning,
                cog_val,
                nom_val,
                cf_val,
            ) = self._compute_employee_status(r, last_by_cf, last_by_name, normalize)

            if not is_monitored:
                count_excluded += 1
            elif diff_days is not None:
                # Conta solo i dipendenti monitorati per gli stati attivi
                if diff_days <= 20:
                    count_ok += 1
                elif diff_days <= 30:
                    count_warning += 1
                else:
                    count_expired += 1

            if self.current_filter:
                # Gestione filtro "Esclusi"
                if self.current_filter == "excluded":
                    if is_monitored:
                        continue
                # Gestione filtri stati (ok, warning, expired) - mostrano solo i monitorati
                elif self.current_filter in ["ok", "warning", "expired"]:
                    if not is_monitored:
                        continue
                    
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

            inactivation_val = 30 - diff_days if diff_days is not None else None
            display_cognome = f"⚠️ {r[1]}" if cf_warning else r[1]

            master_rows.append(
                [
                    inactivation_val,
                    r[0],
                    display_cognome,
                    r[2],
                    r[7],
                    r[4],
                    r[5],
                    r[3],
                    r[6],
                    r[1],
                ]
            )

        self.card_ok.setValue(count_ok)
        self.card_warning.setValue(count_warning)
        self.card_expired.setValue(count_expired)
        self.card_excluded.setValue(count_excluded)
        return master_rows

    def _build_timbrature_maps(self, accessi):
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

    def _inactivation_formatter(self, value):
        if value is None or value == "":
            return ""
        try:
            days = int(value)
            dot = "●"
            if days < 0:
                days = 0
            return f"{dot} {days}"
        except Exception:
            return str(value)

    def _on_card_filter(self, filter_type):
        # Mappa dei testi professionali per i filtri
        filter_messages = {
            "ok": "Visualizzazione dipendenti operativi (accesso ≤ 20 giorni)",
            "warning": "Visualizzazione dipendenti in scadenza (accesso 21-30 giorni)",
            "expired": "Visualizzazione dipendenti non operativi (accesso > 30 giorni)",
            "excluded": "Visualizzazione dipendenti esclusi dal monitoraggio",
        }

        if self.current_filter == filter_type:
            self.current_filter = None
            ToastManager.instance().show(
                "Filtro disattivato - Visualizzazione completa", "info", duration=2500
            )
        else:
            self.current_filter = filter_type
            message = filter_messages.get(filter_type, f"Filtro: {filter_type}")
            ToastManager.instance().show(message, "info", duration=3000)

        for card in [
            self.card_ok,
            self.card_warning,
            self.card_expired,
            self.card_excluded,
        ]:
            is_active = card.filter_type == self.current_filter
            gradient = (
                "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #e8f5e9, stop:1 #f8f9fa)"
                if is_active
                else "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 white, stop:1 #fafbfc)"
            )
            style = f"background: {gradient}; border: {'3px' if is_active else '2px'} solid {card.base_color}; border-radius: 12px;"
            card.setStyleSheet(f"InteractiveStatusCard {{ {style} }}")
        self.refresh_data()

    def _on_selection_changed(self, selected, _deselected):
        indexes = self.table.selectionModel().selectedRows()
        if not indexes:
            return
        row_idx = indexes[0].row()
        row_data = self.model._data[row_idx]

        mapping = {
            "ID Risorsa": 1,
            "Cognome": 9,
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
            if h == "Importato il":
                val = self._format_db_date(val)

            if h in self.detail_labels and self.detail_labels[h]:
                self.detail_labels[h].setText(val)

        access_info, _, color = self._get_last_isab_access(cognome, nome)
        self.last_access_label.setText(access_info)
        self.last_access_label.setStyleSheet(
            f"color: {color}; font-weight: bold; font-size: 14px; padding: 5px 0;"
        )

    def _format_db_date(self, date_str):
        if not date_str or date_str == "None":
            return "-"
        try:
            return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").strftime(
                "%d/%m/%Y %H:%M:%S"
            )
        except Exception:
            return date_str

    def _get_last_isab_access(self, cognome, nome):
        norm_cognome = self._normalize_name(cognome)
        norm_nome = self._normalize_name(nome)
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
                return "Mai effettuato", "-", "#6c757d"

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

            delta = (datetime.now() - last_date).days
            formatted_date = last_date.strftime("%d/%m/%Y")

            if delta <= 20:
                return f"{formatted_date} ({delta} gg fa)", str(delta), "#198754"
            elif delta <= 30:
                return f"{formatted_date} ({delta} gg fa)", str(delta), "#fd7e14"
            else:
                return (
                    f"{formatted_date} (SCADUTA - {delta} gg fa)",
                    str(delta),
                    "#dc3545",
                )
        except Exception as e:
            logger.error(f"Errore recupero ultimo accesso ISAB: {e}")
            return "Errore", "-", "#6c757d"

    def _normalize_name(self, text):
        if not text:
            return ""
        return re.sub(r"\s+", " ", str(text).strip().upper())

    def _on_import_clicked(self):
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
                count = 0
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
                    count += 1
            ToastManager.instance().show(
                f"Importazione completata: {count} dipendenti.", "success"
            )
            self.refresh_data()
        except Exception as e:
            logger.error(f"Errore import CSV: {e}")
            QMessageBox.critical(self, "Errore", f"Impossibile importare:\n{e}")

    def _generate_email_report(self):
        """Genera email report professionale in Outlook con Dashboard e Tabelle."""
        try:
            from src.core.version import __version__

            # 1. Recupero Dati
            # Query per dipendenti (solo monitorati)
            query = """
                SELECT id_risorsa, cognome, nome, codice_fiscale, badge, data_assunzione
                FROM dipendenti
                WHERE monitoraggio_attivo = 1 OR monitoraggio_attivo IS NULL
                ORDER BY cognome ASC, nome ASC
            """
            dipendenti = db_manager.execute_query(db_manager.DB_DIPENDENTI, query)

            # Recupera accessi
            query_timb = "SELECT cognome, nome, codice_fiscale, data FROM timbrature"
            accessi = db_manager.execute_query(db_manager.DB_TIMBRATURE, query_timb)
            last_by_cf, last_by_name, normalize = self._build_timbrature_maps(accessi)

            warning_list = []
            expired_list = []
            
            total_monitored = len(dipendenti)
            
            for dip in dipendenti:
                id_ris, cog, nom, cf, badge, data_ass = dip
                cf_norm = normalize(cf or "")
                name_key = (normalize(cog or ""), normalize(nom or ""))

                diff_days = last_by_cf.get(cf_norm) or last_by_name.get(name_key)
                if diff_days is None:
                    # Se non ha mai fatto accesso o non trovato, lo consideriamo expired? 
                    # Solitamente diff_days is None viene gestito a parte, ma per il report 
                    # manteniamo la logica esistente: se None, lo ignoriamo o mettiamo in expired se vogliamo.
                    # Per coerenza con la tabella GUI, se diff_days è None spesso è "Mai" o "Errore".
                    # Qui li saltiamo per evitare rumore, come prima.
                    continue

                last_access_date = datetime.now() - timedelta(days=diff_days)
                formatted_date = last_access_date.strftime("%d/%m/%Y")
                
                item = {
                    "id": id_ris,
                    "cognome": cog,
                    "nome": nom,
                    "badge": badge if badge else "-",
                    "giorni": diff_days,
                    "data": formatted_date,
                }

                if 21 <= diff_days <= 30:
                    warning_list.append(item)
                elif diff_days > 30:
                    expired_list.append(item)

            # Ordina per urgenza (giorni decrescenti - più urgente prima)
            warning_list.sort(key=lambda x: x["giorni"], reverse=True)
            expired_list.sort(key=lambda x: x["giorni"], reverse=True)

            if not warning_list and not expired_list:
                QMessageBox.information(
                    self,
                    "Nessun dipendente",
                    "Ottimo! Non ci sono dipendenti in scadenza o scaduti.",
                )
                return

            # 2. Costruzione HTML (Layout Moderno & Outlook-Safe)
            current_date = datetime.now().strftime("%d/%m/%Y %H:%M")
            
            # Icona base64
            icon_b64 = ""
            icon_path = Path(get_asset_path("app.ico"))
            if icon_path.exists():
                with open(icon_path, "rb") as f:
                    icon_b64 = base64.b64encode(f.read()).decode("utf-8")
            
            # Stili CSS inline (Outlook friendly)
            font_family = "'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif"
            header_color = "#0d6efd"
            bg_light = "#f8f9fa"
            border_color = "#e5e7eb"

            # Template HTML - Modern SaaS Style
            body_html = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: {font_family}; margin: 0; padding: 0; color: #1f2937; background-color: #f9fafb; }}
                    .container {{ width: auto; max-width: 1500px; margin: 0 auto; background-color: #ffffff; }}
                    .summary-table {{ width: auto; min-width: 480px; border-collapse: separate; border-spacing: 8px; margin: 16px auto; }}
                    .card {{ background-color: #ffffff; padding: 14px 20px; border: 1px solid {border_color}; border-radius: 6px; text-align: center; width: 160px; box-shadow: 0 1px 2px rgba(0,0,0,0.04); }}
                    .card-number {{ font-size: 24px; font-weight: 700; display: block; margin-bottom: 4px; letter-spacing: -0.5px; }}
                    .card-label {{ font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; color: #6b7280; font-weight: 600; }}
                    .data-table {{ width: auto; border-collapse: collapse; margin: 0 0 20px 0; background-color: white; border: 1px solid {border_color}; }}
                    .data-table th {{ background-color: #e7f1ff; text-align: left; padding: 5px 10px; border: 1px solid #cce0ff; font-size: 12px; color: #1a56db; text-transform: uppercase; font-weight: 600; letter-spacing: 0.3px; }}
                    .data-table td {{ padding: 5px 12px; border: 1px solid {border_color}; font-size: 13px; vertical-align: middle; color: #374151; }}
                </style>
            </head>
            <body style="background-color: #f9fafb; margin: 0; padding: 20px 0;">
                <div class="container" style="border-radius: 8px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.08);">
                    <!-- HEADER -->
                    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #0d6efd;">
                        <tr>
                            <td style="padding: 20px 24px; text-align: center;">
                                <h2 style="margin: 0; font-weight: 700; font-size: 20px; color: #ffffff; letter-spacing: -0.3px;">Report Monitoraggio Accessi in ISAB</h2>
                                <p style="margin: 8px 0 0 0; font-size: 13px; font-weight: 400; color: #cfe2ff;">Generato il {current_date} da SyncroJob v{__version__}</p>
                            </td>
                        </tr>
                    </table>

                    <!-- EXECUTIVE SUMMARY -->
                    <div style="padding: 16px 20px; background-color: #ffffff;">
                        <table class="summary-table" style="margin: 0 auto;">
                            <tr>
                                <td style="padding: 4px;">
                                    <div class="card" style="border-left: 3px solid {header_color}; text-align: left;">
                                        <span class="card-number" style="color: #111827;">{total_monitored}</span>
                                        <span class="card-label">Monitorati</span>
                                    </div>
                                </td>
                                <td style="padding: 4px;">
                                    <div class="card" style="border-left: 3px solid #f59e0b; text-align: left;">
                                        <span class="card-number" style="color: #111827;">{len(warning_list)}</span>
                                        <span class="card-label">In Scadenza</span>
                                    </div>
                                </td>
                                <td style="padding: 4px;">
                                    <div class="card" style="border-left: 3px solid #ef4444; text-align: left;">
                                        <span class="card-number" style="color: #111827;">{len(expired_list)}</span>
                                        <span class="card-label">Scaduti</span>
                                    </div>
                                </td>
                            </tr>
                        </table>
                    </div>
            """

            # Calcolare frase riassuntiva dinamica con urgenza
            urgenti = len([d for d in expired_list if d["giorni"] > 60])
            totale_attenzione = len(warning_list) + len(expired_list)

            if urgenti > 0:
                summary_text = f"<strong>ATTENZIONE:</strong> {urgenti} dipendenti richiedono azione <strong>IMMEDIATA</strong> (oltre 60 giorni). Totale da gestire: {totale_attenzione}."
                summary_color = "#dc3545"
                summary_icon = "⚠️"
            elif len(expired_list) > 0:
                summary_text = f"<strong>{len(expired_list)}</strong> dipendenti scaduti e <strong>{len(warning_list)}</strong> in scadenza richiedono attenzione."
                summary_color = "#fd7e14"
                summary_icon = "🚨"
            else:
                summary_text = f"<strong>{len(warning_list)}</strong> dipendenti in scadenza da monitorare nei prossimi giorni."
                summary_color = "#0d6efd"
                summary_icon = "ℹ️"

            # Calcolo trend rispetto al report precedente
            trend_html = ""
            trend = ReportHistory.calculate_trend(len(warning_list), len(expired_list))
            if trend:
                trend_parts = []
                warning_diff = trend["warning_diff"]
                expired_diff = trend["expired_diff"]

                if warning_diff > 0:
                    trend_parts.append(f'<span style="color: #dc3545;">+{warning_diff} in scadenza</span>')
                elif warning_diff < 0:
                    trend_parts.append(f'<span style="color: #198754;">{warning_diff} in scadenza</span>')

                if expired_diff > 0:
                    trend_parts.append(f'<span style="color: #dc3545;">+{expired_diff} scaduti</span>')
                elif expired_diff < 0:
                    trend_parts.append(f'<span style="color: #198754;">{expired_diff} scaduti</span>')

                if trend_parts:
                    trend_text = " | ".join(trend_parts)
                    trend_html = f'<p style="margin: 8px 0 0 0; padding: 10px 12px; background-color: #f8f9fa; border-radius: 4px; font-size: 12px; color: #6b7280;">📊 <strong>Trend:</strong> {trend_text} rispetto al {trend["last_date"]}</p>'

            body_html += '<div style="padding: 0 20px 20px 20px; background-color: #ffffff;">'
            body_html += f'<p style="margin: 0 0 8px 0; padding: 12px; background-color: #fff8f0; border-radius: 6px; color: {summary_color}; font-size: 13px; border-left: 3px solid {summary_color}; font-weight: 500;">'
            body_html += f'{summary_icon} {summary_text}</p>'
            body_html += trend_html

            def build_multi_column_table(data_list, color, rows_per_col=10):
                """Genera tabelle affiancate con max righe per colonna."""
                if not data_list:
                    return ""

                # Dividi in chunk
                chunks = [data_list[i:i + rows_per_col] for i in range(0, len(data_list), rows_per_col)]
                num_cols = min(len(chunks), 4)  # Max 4 colonne

                html = '<table cellpadding="0" cellspacing="0" border="0"><tr>'

                for col_idx, chunk in enumerate(chunks[:4]):
                    if col_idx > 0:
                        html += '<td style="width: 15px;"></td>'  # Spaziatura

                    html += '<td style="vertical-align: top;">'
                    html += f'''<table class="data-table">
                        <thead>
                            <tr>
                                <th>Dipendente</th>
                                <th>Badge</th>
                                <th>Ultimo Accesso</th>
                                <th style="text-align: center;">Gg</th>
                            </tr>
                        </thead>
                        <tbody>'''

                    for idx, dip in enumerate(chunk):
                        row_bg = "#ffffff" if idx % 2 == 0 else "#f8f9fa"
                        html += f'''<tr style="background-color: {row_bg};">
                            <td style="font-weight: 500; color: #1f2937;">{dip['cognome']} {dip['nome']}</td>
                            <td style="color: #4b5563;">{dip['badge']}</td>
                            <td style="color: #4b5563;">{dip['data']}</td>
                            <td style="text-align: center; color: {color}; font-weight: 600;">{dip['giorni']}</td>
                        </tr>'''

                    html += '</tbody></table></td>'

                html += '</tr></table>'
                return html

            # Sezione EXPIRING (Warning)
            if warning_list:
                body_html += f"""
                    <div style="margin-bottom: 20px;">
                        <h3 style="color: #fd7e14; margin: 16px 0 12px 0; padding-left: 12px; border-left: 4px solid #fd7e14; font-size: 15px; font-weight: 600;">⚠️ In Scadenza (21-30 gg)</h3>
                """
                body_html += build_multi_column_table(warning_list, "#fd7e14")
                body_html += "</div>"

            # Sezione EXPIRED (Scaduti)
            if expired_list:
                body_html += f"""
                    <div style="margin-bottom: 20px;">
                        <h3 style="color: #dc3545; margin: 16px 0 12px 0; padding-left: 12px; border-left: 4px solid #dc3545; font-size: 15px; font-weight: 600;">🚫 Scaduti (&gt; 30 gg)</h3>
                """
                body_html += build_multi_column_table(expired_list, "#dc3545")
                body_html += "</div>"

            # Footer
            body_html += f"""
                    </div>
                </div>
            </body>
            </html>
            """

            subject = f"Report Monitoraggio Accessi in ISAB - {datetime.now().strftime('%d/%m/%Y')}"

            # 3. Creazione allegato Excel con tutti i dati
            excel_path = None
            if warning_list or expired_list:
                excel_data = []
                for dip in warning_list:
                    excel_data.append({
                        "Cognome": dip["cognome"],
                        "Nome": dip["nome"],
                        "Badge": dip["badge"],
                        "Ultimo Accesso": dip["data"],
                        "Giorni": dip["giorni"],
                        "Stato": "In Scadenza"
                    })
                for dip in expired_list:
                    excel_data.append({
                        "Cognome": dip["cognome"],
                        "Nome": dip["nome"],
                        "Badge": dip["badge"],
                        "Ultimo Accesso": dip["data"],
                        "Giorni": dip["giorni"],
                        "Stato": "Scaduto"
                    })

                df_report = pd.DataFrame(excel_data)
                excel_path = Path(os.environ["TEMP"]) / f"report Accessi ISAB {datetime.now().strftime('%d-%m-%Y_%H-%M')}.xlsx"
                df_report.to_excel(excel_path, index=False, sheet_name="Dipendenti")

            # 4. Invio (Outlook / Fallback)
            if os.name == "nt":
                try:
                    import win32com.client
                    outlook = win32com.client.Dispatch("Outlook.Application")
                    mail = outlook.CreateItem(0)
                    mail.To = "luca.riccio@coemi.it"
                    mail.CC = "isabsud@coemi.it"
                    mail.Subject = subject
                    mail.HTMLBody = body_html

                    # Aggiungi allegato Excel se presente
                    if excel_path and excel_path.exists():
                        mail.Attachments.Add(str(excel_path))

                    mail.Display()

                    # Salva snapshot del report per il calcolo del trend futuro
                    ReportHistory.save_report(warning_list, expired_list)

                    ToastManager.instance().show("Report generato in Outlook con allegato Excel", "success", duration=3000)
                except Exception as e:
                    # Fallback per problemi COM o Outlook non configurato
                    logger.warning(f"Fallback Outlook failed: {e}")
                    import webbrowser
                    # Mailto non supporta body HTML complessi, apriamo un file temporaneo nel browser
                    # che l'utente può copiare/stampare o salvare come PDF
                    tmp_path = Path(os.environ["TEMP"]) / "report_isab.html"
                    with open(tmp_path, "w", encoding="utf-8") as f:
                        f.write(body_html)
                    webbrowser.open(f"file:///{tmp_path.as_posix()}")

                    # Salva snapshot anche in fallback
                    ReportHistory.save_report(warning_list, expired_list)

                    ToastManager.instance().show("Outlook non trovato: aperto report nel browser", "warning", duration=4000)

            else:
                # Fallback non-Windows (debug)
                ToastManager.instance().show("Invio email disponibile solo su Windows/Outlook", "error", duration=3000)

        except Exception as e:
            logger.error(f"Errore generazione email report: {e}")
            QMessageBox.critical(self, "Errore", f"Impossibile generare il report:\n{e}")
