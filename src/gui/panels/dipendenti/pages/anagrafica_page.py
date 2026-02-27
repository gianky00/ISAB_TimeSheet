import csv
import logging
from datetime import UTC, datetime

from src.gui.widgets.core_widgets import PrimaryButton, SecondaryButton, SearchInput, FilterComboBox, StandardTable, DangerButton
from PyQt6.QtCore import (
    QDate,
    Qt,
    QTimer,
)
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QSizePolicy,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from src.bots import create_bot
from src.core import config_manager
from src.core.constants import Icons
from src.core.database import db_manager
from src.core.sync_tracker import SyncTracker
from src.gui.formatters import FastTableModel
from src.gui.panels.base import BotWorker
from src.gui.panels.dipendenti.shared import (
    ColoredDotDelegate,
    InteractiveStatusCard,
)
from src.gui.panels.dipendenti.utils.data_helpers import (
    build_timbrature_maps,
    compute_employee_status,
    format_db_date,
    normalize_name,
)
from src.gui.panels.dipendenti.utils.report_generator import ReportGenerator
from src.gui.panels.dipendenti.widgets.employee_detail_view import EmployeeDetailView
from src.gui.styles import COLORS
from src.gui.widgets.modern_button import ModernButton
from src.gui.widgets.toast import ToastManager
from src.utils.helpers import get_asset_path, get_colored_icon

logger = logging.getLogger(__name__)


class AnagraficaPage(QWidget):
    """Pagina per la visualizzazione e gestione anagrafica dipendenti."""

    def __init__(self, parent=None):
        super().__init__(parent)

        # Widget members (Strict Typing - Option D)
        self.search_input: QLineEdit
        self.lbl_sync_status: QLabel
        self.btn_bot_update: ModernButton
        self.cards_container: QWidget
        self.card_ok: InteractiveStatusCard
        self.card_warning: InteractiveStatusCard
        self.card_expired: InteractiveStatusCard
        self.card_excluded: InteractiveStatusCard
        self.table: QTableView
        self.detail_view: EmployeeDetailView

        self.worker: BotWorker | None = None
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
        main_layout.setSpacing(15)

        # 1. Filtri e Azioni (Design Modern Card)
        self.filter_card = QFrame()
        self.filter_card.setObjectName("filterBar")
        self.filter_card.setStyleSheet(f"""
            QFrame#filterBar {{
                background-color: {COLORS["bg_white"]};
                border: 1px solid {COLORS["border_light"]};
                border-radius: 12px;
            }}
        """)
        filter_layout = QHBoxLayout(self.filter_card)
        filter_layout.setContentsMargins(15, 10, 15, 10)
        filter_layout.setSpacing(15)

        # Sezione Ricerca
        search_v = QVBoxLayout()
        search_v.setSpacing(4)
        search_label = QLabel("CERCA DIPENDENTE")
        from src.gui.styles import LABEL_MUTED, LINEEDIT_STYLE
        search_label.setStyleSheet(LABEL_MUTED)
        self.search_input = SearchInput()
        self.search_input.setPlaceholderText("Nome, Cognome, CF o Badge...")
        self.search_input.setMinimumWidth(300)
        self.search_input.setStyleSheet(LINEEDIT_STYLE)
        self.search_input.textChanged.connect(lambda: self.search_timer.start(500))
        search_v.addWidget(search_label)
        search_v.addWidget(self.search_input)
        filter_layout.addLayout(search_v)

        filter_layout.addStretch()

        # Info & Actions
        info_v = QVBoxLayout()
        info_v.setSpacing(4)
        info_v.setAlignment(Qt.AlignmentFlag.AlignRight)

        # Sync Status Label
        self.lbl_sync_status = QLabel("")
        self.lbl_sync_status.setStyleSheet(
            f"color: {COLORS['text_muted']}; font-size: 10px;"
        )
        info_v.addWidget(self.lbl_sync_status)

        actions_h = QHBoxLayout()
        actions_h.setSpacing(8)

        import_btn = ModernButton(
            "IMPORTA CSV",
            variant=ModernButton.Variant.GHOST,
            size=ModernButton.Size.SMALL,
            icon=get_asset_path(Icons.UPLOAD),
        )
        import_btn.clicked.connect(self._on_import_clicked)

        email_report_btn = ModernButton(
            "REPORT EMAIL",
            variant=ModernButton.Variant.GHOST,
            size=ModernButton.Size.SMALL,
            icon=get_asset_path(Icons.SEND),
        )
        email_report_btn.clicked.connect(self._generate_email_report)

        # Update Bot Button
        self.btn_bot_update = ModernButton(
            "AGGIORNA",
            variant=ModernButton.Variant.PRIMARY,
            size=ModernButton.Size.SMALL,
            icon=get_asset_path(Icons.REFRESH),
        )
        self.btn_bot_update.clicked.connect(self._on_update_bot_clicked)

        actions_h.addWidget(import_btn)
        actions_h.addWidget(email_report_btn)
        actions_h.addWidget(self.btn_bot_update)
        info_v.addLayout(actions_h)

        filter_layout.addLayout(info_v)
        main_layout.addWidget(self.filter_card)

        # Cards Container
        self.cards_container = QWidget()
        cards_layout = QHBoxLayout(self.cards_container)
        cards_layout.setContentsMargins(0, 5, 0, 5)
        cards_layout.setSpacing(15)

        self.card_ok = InteractiveStatusCard(
            "Operativi", COLORS["success_dark"], Icons.CHECK_CIRCLE, "Ultimo accesso ≤20gg", "ok"
        )
        self.card_warning = InteractiveStatusCard(
            "In Scadenza",
            COLORS["warning_orange"],
            Icons.ALERT_TRIANGLE,
            "Accesso 21-30gg fa",
            "warning",
        )
        self.card_expired = InteractiveStatusCard(
            "Scaduti", COLORS["error_red"], Icons.X_CIRCLE, "Accesso >30gg fa", "expired"
        )
        self.card_excluded = InteractiveStatusCard(
            "Esclusi",
            COLORS["text_muted"],
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
        v_header = self.table.verticalHeader()
        if v_header is None:
            raise RuntimeError("Table vertical header is None")
        v_header.setVisible(False)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.table.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.table.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)

        # Menu contestuale per bypass monitoraggio
        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self._show_context_menu)

        header = self.table.horizontalHeader()
        if header is None:
            raise RuntimeError("Table horizontal header is None")
        selection_model = self.table.selectionModel()
        if selection_model is None:
            raise RuntimeError("Table selection model is None")
        selection_model.selectionChanged.connect(self._on_selection_changed)
        self.table.setItemDelegateForColumn(0, ColoredDotDelegate(self.table))

        # Larghezze colonne
        self.column_widths = [80, 100, 200, 150, 180, 100, 145]
        for col_idx in range(len(self.column_widths)):
            header.setSectionResizeMode(col_idx, QHeaderView.ResizeMode.Fixed)
            self.table.setColumnWidth(col_idx, self.column_widths[col_idx])

        total_width = sum(self.column_widths) + 20
        self.table.setFixedWidth(total_width)

        # Imposta la larghezza delle card uguale a quella della tabella
        self.cards_container.setFixedWidth(total_width)

        self.content_layout.addWidget(self.table)

        # Pannello Destra (Scheda Dettagli)
        self.detail_view = EmployeeDetailView()
        self.content_layout.addWidget(self.detail_view)
        self.content_layout.addStretch()

        main_layout.addLayout(self.content_layout)

    def _show_context_menu(self, position):
        """Mostra menu contestuale per gestione monitoraggio dipendente."""
        selection_model = self.table.selectionModel()
        if selection_model is None:
            raise RuntimeError("Table selection model is None")
        indexes = selection_model.selectedRows()
        if not indexes:
            return

        row_idx = indexes[0].row()
        row_data = self.model._data[row_idx]
        id_risorsa = row_data[1]  # ID Risorsa

        # Verifica stato monitoraggio corrente
        query = "SELECT monitoraggio_attivo FROM dipendenti WHERE id_risorsa = ?"
        result = db_manager.execute_query(db_manager.DB_DIPENDENTI, query, (id_risorsa,))
        is_monitored = result[0][0] if result and result[0][0] is not None else 1

        from PyQt6.QtGui import QAction
        from PyQt6.QtWidgets import QMenu

        menu = QMenu(self)

        if is_monitored:
            action = QAction(
                get_colored_icon(get_asset_path(Icons.X_CIRCLE), COLORS["error_red"]),
                "🚫 Escludi da monitoraggio",
                self,
            )
            action.triggered.connect(lambda: self._toggle_monitoring(id_risorsa, False))
        else:
            action = QAction(
                get_colored_icon(get_asset_path(Icons.CHECK_CIRCLE), COLORS["success_dark"]),
                "✅ Riattiva monitoraggio",
                self,
            )
            action.triggered.connect(lambda: self._toggle_monitoring(id_risorsa, True))

        menu.addAction(action)
        viewport = self.table.viewport()
        if viewport is None:
            raise RuntimeError("Table viewport is None")
        menu.exec(viewport.mapToGlobal(position))

    def _toggle_monitoring(self, id_risorsa, enable):
        """Attiva o disattiva il monitoraggio per un dipendente."""
        try:
            query = "UPDATE dipendenti SET monitoraggio_attivo = ? WHERE id_risorsa = ?"
            db_manager.execute_query(db_manager.DB_DIPENDENTI, query, (1 if enable else 0, id_risorsa))

            status_text = "riattivato" if enable else "escluso"
            ToastManager.instance().show(
                f"Monitoraggio {status_text} per il dipendente",
                "success",
                duration=2500,
            )
            self.refresh_data()
        except Exception as e:
            logger.error(f"Errore toggle monitoraggio: {e}")
            QMessageBox.critical(self, "Errore", f"Impossibile modificare il monitoraggio:\n{e}")

    def refresh_data(self):
        """Aggiorna i dati della tabella dipendenti caricandoli dal database e applicando i filtri correnti."""
        self.lbl_sync_status.setText(f"Ultimo Sync: {SyncTracker.get_formatted_status('timbrature')}")
        search_text = self.search_input.text().lower().strip()
        query = """
            SELECT id_risorsa, cognome, nome, data_nascita, badge, data_assunzione, created_at, codice_fiscale, monitoraggio_attivo
            FROM dipendenti WHERE 1=1
        """
        params = []

        if search_text:
            terms = search_text.split()
            for term in terms:
                p = f"%{term}%"
                query += " AND (cognome LIKE ? OR nome LIKE ? OR badge LIKE ? OR codice_fiscale LIKE ?)"
                params.extend([p, p, p, p])

        query += " ORDER BY cognome ASC, nome ASC"

        header = self.table.horizontalHeader()
        if header is None:
            raise RuntimeError("Table horizontal header is None")
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)

        try:
            full_rows = db_manager.execute_query(db_manager.DB_DIPENDENTI, query, tuple(params))
            master_rows = self._process_employee_rows(full_rows)
            self.model.update_data(master_rows)
            self.model.set_column_formatter(0, self._inactivation_formatter)
            self.model.set_column_alignment(0, Qt.AlignmentFlag.AlignCenter)
        except Exception as e:
            logger.error(f"Errore caricamento dipendenti: {e}")

    def _process_employee_rows(self, full_rows):
        query_timb = "SELECT cognome, nome, codice_fiscale, data FROM timbrature"
        accessi = db_manager.execute_query(db_manager.DB_TIMBRATURE, query_timb)
        last_by_cf, last_by_name, normalize = build_timbrature_maps(accessi)

        master_rows = []
        counts = {"ok": 0, "warning": 0, "expired": 0, "excluded": 0}

        for r in full_rows:
            is_monitored = r[8] if len(r) > 8 and r[8] is not None else 1
            diff_days, cf_warning, _, _, _ = compute_employee_status(r, last_by_cf, last_by_name, normalize)

            # 1. Aggiornamento Conteggi
            self._update_status_counts(counts, is_monitored, diff_days)

            # 2. Applicazione Filtri UI
            if self._should_skip_by_filter(is_monitored, diff_days):
                continue

            # 3. Formattazione riga
            from src.gui.styles.constants import THRESHOLD_DAYS

            inactivation_val = THRESHOLD_DAYS["expired"] - diff_days if diff_days is not None else None
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

        # Aggiorna le card UI
        self.card_ok.setValue(counts["ok"])
        self.card_warning.setValue(counts["warning"])
        self.card_expired.setValue(counts["expired"])
        self.card_excluded.setValue(counts["excluded"])
        return master_rows

    def _update_status_counts(self, counts, is_monitored, diff_days):
        """Aggiorna i contatori degli stati per le card UI."""
        from src.gui.styles.constants import THRESHOLD_DAYS

        if not is_monitored:
            counts["excluded"] += 1
        elif diff_days is not None:
            if diff_days <= THRESHOLD_DAYS["warning"]:
                counts["ok"] += 1
            elif diff_days <= THRESHOLD_DAYS["expired"]:
                counts["warning"] += 1
            else:
                counts["expired"] += 1

    def _should_skip_by_filter(self, is_monitored, diff_days):
        """Determina se un dipendente deve essere escluso dalla vista in base al filtro attivo."""
        if not self.current_filter:
            return False

        from src.gui.styles.constants import THRESHOLD_DAYS

        if self.current_filter == "excluded":
            return bool(is_monitored)

        # Per gli altri filtri (ok, warning, expired), mostriamo solo i monitorati con dati validi
        if not is_monitored or diff_days is None:
            return True

        if self.current_filter == "ok" and diff_days > THRESHOLD_DAYS["warning"]:
            return True
        if self.current_filter == "warning" and (
            diff_days <= THRESHOLD_DAYS["warning"] or diff_days > THRESHOLD_DAYS["expired"]
        ):
            return True
        return bool(self.current_filter == "expired" and diff_days <= THRESHOLD_DAYS["expired"])

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

        for card in (
            self.card_ok,
            self.card_warning,
            self.card_expired,
            self.card_excluded,
        ):
            is_active = card.filter_type == self.current_filter
            gradient = (
                f"qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {COLORS['bg_success_pastel']}, stop:1 {COLORS['bg_light']})"
                if is_active
                else f"qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {COLORS['bg_white']}, stop:1 {COLORS['bg_alt']})"
            )
            style = f"background: {gradient}; border: {'3px' if is_active else '2px'} solid {card.base_color}; border-radius: 12px;"
            card.setStyleSheet(f"InteractiveStatusCard {{ {style} }}")
        self.refresh_data()

    def _on_selection_changed(self, selected, _deselected):
        """Aggiorna la scheda dettagli quando cambia la riga selezionata in tabella."""
        selection_model = self.table.selectionModel()
        if selection_model is None:
            raise RuntimeError("Table selection model is None")
        indexes = selection_model.selectedRows()
        if not indexes:
            self.detail_view.reset()
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

        details_dict = {}
        for h, idx in mapping.items():
            val = str(row_data[idx]) if idx is not None and row_data[idx] is not None else ""
            if val.lower() in ("nan", "none"):
                val = ""
            if h == "Importato il":
                val = format_db_date(val)
            details_dict[h] = val

        cognome = str(row_data[9])
        nome = str(row_data[3])
        access_info = self._get_last_isab_access(cognome, nome)

        self.detail_view.update_data(details_dict, access_info)

    def _get_last_isab_access(self, cognome, nome):
        """
        Recupera la data dell'ultimo accesso ISAB dal database delle timbrature.

        Returns:
            tuple: (stringa formattata, giorni trascorsi, colore stato).
        """
        norm_cognome = normalize_name(cognome)
        norm_nome = normalize_name(nome)
        query = """
            SELECT data FROM timbrature
            WHERE UPPER(REPLACE(REPLACE(TRIM(cognome), '  ', ' '), '  ', ' ')) = ?
              AND UPPER(REPLACE(REPLACE(TRIM(nome), '  ', ' '), '  ', ' ')) = ?
            ORDER BY data DESC LIMIT 1
        """
        try:
            res = db_manager.execute_query(db_manager.DB_TIMBRATURE, query, (norm_cognome, norm_nome))
            if not res:
                return "Mai effettuato", "-", COLORS["text_muted"]

            last_date_str = str(res[0][0])
            date_part = last_date_str.split(" ")[0]
            last_date = None
            for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
                try:
                    last_date = datetime.strptime(date_part, fmt).replace(tzinfo=UTC)
                    break
                except ValueError:
                    continue

            if not last_date:
                return "Errore data", "-", COLORS["text_muted"]

            delta = (datetime.now() - last_date).days
            formatted_date = last_date.strftime("%d/%m/%Y")

            from src.gui.styles.constants import THRESHOLD_DAYS

            if delta <= THRESHOLD_DAYS["warning"]:
                return f"{formatted_date} ({delta} gg fa)", str(delta), COLORS["success_dark"]
            if delta <= THRESHOLD_DAYS["expired"]:
                return f"{formatted_date} ({delta} gg fa)", str(delta), COLORS["warning_orange"]
            return (
                f"{formatted_date} (SCADUTA - {delta} gg fa)",
                str(delta),
                COLORS["error_red"],
            )
        except Exception as e:
            logger.error(f"Errore recupero ultimo accesso ISAB: {e}")
            return "Errore", "-", COLORS["text_muted"]

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
            with open(file_path, encoding="utf-8-sig") as f:
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

            # Aggiorna SyncTracker per i dipendenti
            SyncTracker.update_status("dipendenti", added=count, removed=0)

            ToastManager.instance().show(f"Importazione completata: {count} dipendenti.", "success")
            self.refresh_data()
        except Exception as e:
            logger.error(f"Errore import CSV: {e}")
            QMessageBox.critical(self, "Errore", f"Impossibile importare:\n{e}")

    def _generate_email_report(self):
        ReportGenerator.generate_email_report(self)

    def _on_update_bot_clicked(self):
        """Avvia il bot Timbrature con date automatiche."""
        try:
            # 1. Recupera Credenziali
            account = config_manager.get_default_account()
            if not account:
                QMessageBox.warning(self, "Attenzione", "Credenziali SafeWork non configurate.")
                return
            username, password = account.get("username"), account.get("password")

            # 2. Calcola Date
            last_date_str = None
            try:
                query = "SELECT MAX(data) FROM timbrature"
                with db_manager.get_connection(db_manager.DB_TIMBRATURE, read_only=True) as conn:
                    res = conn.execute(query).fetchone()
                    if res and res[0]:
                        last_date_str = res[0]
            except Exception as e:
                logger.error(f"Errore query data: {e}")

            if last_date_str:
                try:
                    last_date = QDate.fromString(last_date_str, "yyyy-MM-dd")
                    start_date = last_date.addDays(1)
                except Exception:
                    start_date = QDate.currentDate().addDays(-30)
            else:
                start_date = QDate.currentDate().addDays(-30)

            end_date = QDate.currentDate().addDays(-1)  # Ieri

            if start_date > end_date:
                if not self._show_confirmation_dialog(
                    "Database Aggiornato",
                    "Il database è aggiornato fino a ieri. Procedere comunque?",
                    cancel_text="No",
                    confirm_text="Sì",
                ):
                    return
                # Se l'utente vuole procedere, forziamo il download di ieri
                start_date = end_date

            data_da_fmt = start_date.toString("dd.MM.yyyy")
            data_a_fmt = end_date.toString("dd.MM.yyyy")

            from src.core.constants import Business

            config = config_manager.load_config()
            fornitore = config.get("last_timbrature_fornitore", Business.DEFAULT_SUPPLIER)

            # 3. Conferma
            msg = f"Aggiornare timbrature dal <b>{data_da_fmt}</b> al <b>{data_a_fmt}</b>?<br>Fornitore: {fornitore}"
            if not self._show_confirmation_dialog("Scarico Timbrature", msg):
                return

            self.btn_bot_update.setEnabled(False)
            ToastManager.instance().show("Avvio Bot Timbrature...", "info")

            # 4. Avvia Bot
            bot = create_bot(
                "timbrature",
                username=username,
                password=password,
                headless=config.get("browser_headless", False),
                timeout=config.get("browser_timeout", 30),
                download_path=str(config_manager.CONFIG_DIR / "temp"),
                data_da=data_da_fmt,
                data_a=data_a_fmt,
                fornitore=fornitore,
            )

            if not bot:
                self.btn_bot_update.setEnabled(True)
                return

            bot_data = {
                "data_da": data_da_fmt,
                "data_a": data_a_fmt,
                "fornitore": fornitore,
            }
            self.worker = BotWorker(bot, bot_data)
            self.worker.finished_signal.connect(self._on_bot_finished)
            self.worker.start()

        except Exception as e:
            self.btn_bot_update.setEnabled(True)
            QMessageBox.critical(self, "Errore", f"Errore avvio bot: {e}")

    def _on_bot_finished(self, success: bool):
        self.btn_bot_update.setEnabled(True)
        if success:
            ToastManager.instance().show("Timbrature scaricate!", "success")
            self.refresh_data()
        else:
            QMessageBox.warning(self, "Errore", "Bot terminato con errori.")

    def _show_confirmation_dialog(
        self, title: str, message: str, cancel_text="Annulla", confirm_text="Avvia"
    ) -> bool:
        """Mostra una dialog di conferma con stile coerente."""
        try:
            dlg = QDialog(self)
            dlg.setWindowTitle(title)
            dlg.setMinimumWidth(350)
            dlg.setWindowFlags(dlg.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)

            layout = QVBoxLayout(dlg)
            layout.setSpacing(20)
            layout.setContentsMargins(20, 20, 20, 20)

            lbl = QLabel(message)
            lbl.setWordWrap(True)
            lbl.setTextFormat(Qt.TextFormat.RichText)
            layout.addWidget(lbl)

            btn_layout = QHBoxLayout()
            btn_layout.addStretch()

            btn_cancel = ModernButton(cancel_text, variant=ModernButton.Variant.GHOST)
            btn_cancel.clicked.connect(dlg.reject)
            btn_confirm = ModernButton(confirm_text, variant=ModernButton.Variant.PRIMARY)
            btn_confirm.clicked.connect(dlg.accept)

            btn_layout.addWidget(btn_cancel)
            btn_layout.addWidget(btn_confirm)
            layout.addLayout(btn_layout)

            return dlg.exec() == 1
        except Exception:
            return False
