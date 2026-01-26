import csv
import logging
import re
from contextlib import suppress
from datetime import datetime, timedelta

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

        self.card_ok.clicked.connect(self._on_card_filter)
        self.card_warning.clicked.connect(self._on_card_filter)
        self.card_expired.clicked.connect(self._on_card_filter)

        cards_layout.addWidget(self.card_ok, stretch=1)
        cards_layout.addWidget(self.card_warning, stretch=1)
        cards_layout.addWidget(self.card_expired, stretch=1)

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

            # Conta solo i dipendenti monitorati
            if diff_days is not None and is_monitored:
                if diff_days <= 20:
                    count_ok += 1
                elif diff_days <= 30:
                    count_warning += 1
                else:
                    count_expired += 1

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

        for card in [self.card_ok, self.card_warning, self.card_expired]:
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
        """Genera email report professionale in Outlook con dipendenti in scadenza e scaduti."""
        try:
            import urllib.parse

            # Query per dipendenti warning e expired (solo monitorati)
            query = """
                SELECT id_risorsa, cognome, nome, codice_fiscale, badge, data_assunzione
                FROM dipendenti
                WHERE monitoraggio_attivo = 1 OR monitoraggio_attivo IS NULL
                ORDER BY cognome ASC, nome ASC
            """
            dipendenti = db_manager.execute_query(db_manager.DB_DIPENDENTI, query)

            # Recupera accessi per calcolare stato
            query_timb = "SELECT cognome, nome, codice_fiscale, data FROM timbrature"
            accessi = db_manager.execute_query(db_manager.DB_TIMBRATURE, query_timb)
            last_by_cf, last_by_name, normalize = self._build_timbrature_maps(accessi)

            warning_list = []
            expired_list = []

            for dip in dipendenti:
                id_ris, cog, nom, cf, badge, data_ass = dip
                cf_norm = normalize(cf or "")
                name_key = (normalize(cog or ""), normalize(nom or ""))

                # last_by_cf e last_by_name contengono giorni (int), non datetime
                diff_days = last_by_cf.get(cf_norm) or last_by_name.get(name_key)
                if diff_days is None:
                    continue

                # Calcola la data effettiva dell'ultimo accesso
                last_access_date = datetime.now() - timedelta(days=diff_days)
                formatted_date = last_access_date.strftime("%d/%m/%Y")

                if 21 <= diff_days <= 30:
                    warning_list.append(
                        {
                            "id": id_ris,
                            "cognome": cog,
                            "nome": nom,
                            "badge": badge,
                            "giorni": diff_days,
                            "data": formatted_date,
                        }
                    )
                elif diff_days > 30:
                    expired_list.append(
                        {
                            "id": id_ris,
                            "cognome": cog,
                            "nome": nom,
                            "badge": badge,
                            "giorni": diff_days,
                            "data": formatted_date,
                        }
                    )

            if not warning_list and not expired_list:
                QMessageBox.information(
                    self,
                    "Nessun dipendente",
                    "Non ci sono dipendenti in scadenza o scaduti da segnalare.",
                )
                return

            # Costruisci corpo email HTML
            current_date = datetime.now().strftime("%d/%m/%Y %H:%M")
            body_html = f"""<html><body style='font-family: Arial, sans-serif;'>
<h2 style='color: #0d6efd;'>Report Monitoraggio Dipendenti ISAB</h2>
<p><strong>Data generazione:</strong> {current_date}</p>
<p><strong>Generato da:</strong> SyncroJob Enterprise</p>
<hr style='border: 1px solid #dee2e6;'>
"""

            if warning_list:
                body_html += f"""
<h3 style='color: #fd7e14;'>⚠️ Dipendenti in Scadenza ({len(warning_list)})</h3>
<p style='font-size: 13px; color: #6c757d;'>Ultimo accesso tra 21 e 30 giorni fa</p>
<table border='1' cellpadding='8' cellspacing='0' style='border-collapse: collapse; width: 100%; font-size: 13px;'>
<thead style='background-color: #fff3cd;'>
<tr>
<th>ID</th><th>Cognome</th><th>Nome</th><th>Badge</th><th>Ultimo Accesso</th><th>Giorni Trascorsi</th>
</tr>
</thead>
<tbody>
"""
                for dip in warning_list:
                    body_html += f"""<tr>
<td>{dip['id']}</td>
<td>{dip['cognome']}</td>
<td>{dip['nome']}</td>
<td>{dip['badge']}</td>
<td>{dip['data']}</td>
<td style='font-weight: bold; color: #fd7e14;'>{dip['giorni']} giorni</td>
</tr>
"""
                body_html += "</tbody></table><br/>"

            if expired_list:
                body_html += f"""
<h3 style='color: #dc3545;'>🚫 Dipendenti Non Operativi ({len(expired_list)})</h3>
<p style='font-size: 13px; color: #6c757d;'>Ultimo accesso oltre 30 giorni fa</p>
<table border='1' cellpadding='8' cellspacing='0' style='border-collapse: collapse; width: 100%; font-size: 13px;'>
<thead style='background-color: #f8d7da;'>
<tr>
<th>ID</th><th>Cognome</th><th>Nome</th><th>Badge</th><th>Ultimo Accesso</th><th>Giorni Trascorsi</th>
</tr>
</thead>
<tbody>
"""
                for dip in expired_list:
                    body_html += f"""<tr>
<td>{dip['id']}</td>
<td>{dip['cognome']}</td>
<td>{dip['nome']}</td>
<td>{dip['badge']}</td>
<td>{dip['data']}</td>
<td style='font-weight: bold; color: #dc3545;'>{dip['giorni']} giorni</td>
</tr>
"""
                body_html += "</tbody></table><br/>"

            body_html += """
<hr style='border: 1px solid #dee2e6;'>
<p style='font-size: 12px; color: #6c757d;'>
<em>Report generato automaticamente da SyncroJob Enterprise.<br/>
Per maggiori informazioni, consultare il sistema di gestione dipendenti.</em>
</p>
</body></html>"""

            # Costruisci mailto URL
            subject = f"Report Monitoraggio Dipendenti ISAB - {current_date}"
            mailto_url = f"mailto:?subject={urllib.parse.quote(subject)}&body={urllib.parse.quote(body_html)}"

            # Apri Outlook (su Windows)
            import os
            import subprocess

            if os.name == "nt":
                subprocess.run(["start", "outlook", mailto_url], shell=True)
            else:
                # Fallback per altri OS
                subprocess.run(["xdg-open", mailto_url])

            ToastManager.instance().show(
                "Email report generata - Outlook aperto", "success", duration=3000
            )

        except Exception as e:
            logger.error(f"Errore generazione email report: {e}")
            QMessageBox.critical(
                self, "Errore", f"Impossibile generare il report email:\n{e}"
            )
