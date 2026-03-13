"""
SyncroJob - Contabilità Panel
Pannello centrale per la visualizzazione e l'analisi della Contabilità Strumentale.
Integra reportistica annuale, dati giornalieri, attività programmate e certificati campione.
Include un motore di ricerca unificato e l'accesso al pannello di analisi KPI.
"""

from contextlib import suppress
from datetime import datetime
from pathlib import Path

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QTableWidget,
    QTabWidget,
    QTreeWidget,
    QVBoxLayout,
    QWidget,
)

from src.core import config_manager
from src.core.constants import Icons
from src.core.contabilita_manager import ContabilitaManager
from src.core.contabilita_worker import ContabilitaWorker
from src.gui.components.animated_tab_widget import AnimatedTabWidget
from src.gui.dialogs.confirmation_dialog import ConfirmationDialog
from src.gui.styles import COLORS
from src.gui.widgets.contabilita.attivita_tab import AttivitaProgrammateTab
from src.gui.widgets.contabilita.certificati_tab import CertificatiCampioneTab
from src.gui.widgets.contabilita.giornaliere_tab import GiornaliereYearTab
from src.gui.widgets.contabilita.year_tab import ContabilitaYearTab
from src.gui.widgets.core_widgets import (
    SearchInput,
)
from src.gui.widgets.modern_button import ModernButton
from src.gui.widgets.modern_card import ModernCard
from src.utils.helpers import get_asset_path, get_colored_icon


class ContabilitaPanel(QWidget):
    """
    Pannello principale dell'interfaccia di contabilità.
    Organizza i dati complessi in tab logici e fornisce strumenti per:
    - Ricerca rapida tra migliaia di record.
    - Calcolo dinamico dei totali ore su selezione utente.
    - Sincronizzazione background con file Excel esterni.
    - Visualizzazione grafica dei KPI.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        """
        Inizializza il pannello e avvia il caricamento lazy dei dati.

        Args:
            parent: Widget genitore opzionale.
        """
        super().__init__(parent)
        self.worker: ContabilitaWorker | None = None
        self.status_labels: list[QLabel] = []
        self.update_buttons: list[ModernButton] = []
        self._last_status_html = "Pronto"
        self._setup_ui()
        QTimer.singleShot(10, self._safe_refresh_tabs)

    def _safe_refresh_tabs(self) -> None:
        """Tenta il caricamento dei tab gestendo eventuali errori critici del DB."""
        try:
            self.refresh_tabs()
        except Exception as e:
            import traceback

            print(f"❌ Error refreshing tabs for ContabilitaPanel: {e}")
            traceback.print_exc()

    def _setup_ui(self) -> None:
        """Costruisce l'architettura dei tab e la toolbar unificata."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        # --- UNIFIED TOOLBAR (Design Modern Card) ---
        self.toolbar_card = ModernCard(elevation=10)
        self.toolbar_card.setObjectName("filterBar")

        toolbar_layout = QHBoxLayout(self.toolbar_card)
        toolbar_layout.setContentsMargins(15, 10, 15, 10)
        toolbar_layout.setSpacing(15)

        from src.gui.styles import LABEL_MUTED, LINEEDIT_STYLE

        # Sezione Statistiche Rapide
        stats_h = QHBoxLayout()
        stats_h.setSpacing(20)

        rows_v = QVBoxLayout()
        rows_v.setSpacing(4)
        lbl_rows = QLabel("RIGHE SELEZIONATE")
        lbl_rows.setStyleSheet(LABEL_MUTED)
        self.selection_count_label = QLabel("0")
        self.selection_count_label.setStyleSheet(
            f"color: {COLORS['text_dark']}; font-weight: 700; font-size: 14px;"
        )
        rows_v.addWidget(lbl_rows)
        rows_v.addWidget(self.selection_count_label)
        stats_h.addLayout(rows_v)

        hours_v = QVBoxLayout()
        hours_v.setSpacing(4)
        lbl_hours = QLabel("TOTALE ORE")
        lbl_hours.setStyleSheet(LABEL_MUTED)
        self.selection_sum_label = QLabel("0")
        self.selection_sum_label.setStyleSheet(
            f"color: {COLORS['teal_accent']}; font-weight: 800; font-size: 14px;"
        )
        hours_v.addWidget(lbl_hours)
        hours_v.addWidget(self.selection_sum_label)
        stats_h.addLayout(hours_v)

        toolbar_layout.addLayout(stats_h)

        # Divisore
        v_line = QFrame()
        v_line.setFrameShape(QFrame.Shape.VLine)
        v_line.setFrameShadow(QFrame.Shadow.Plain)
        v_line.setStyleSheet(f"color: {COLORS['border_light']};")
        toolbar_layout.addWidget(v_line)

        # Sezione Ricerca
        search_v = QVBoxLayout()
        search_v.setSpacing(4)
        lbl_search = QLabel("CERCA NEI DATI")
        lbl_search.setStyleSheet(LABEL_MUTED)
        self.search_input = SearchInput()
        self.search_input.setPlaceholderText("Cerca ovunque...")
        self.search_input.setClearButtonEnabled(True)
        self.search_input.setMinimumWidth(300)
        self.search_input.setStyleSheet(LINEEDIT_STYLE)
        self.search_input.textChanged.connect(self._on_search_changed)
        search_v.addWidget(lbl_search)
        search_v.addWidget(self.search_input)
        toolbar_layout.addLayout(search_v)

        toolbar_layout.addStretch()

        # Info & Actions
        info_v = QVBoxLayout()
        info_v.setSpacing(4)
        info_v.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.status_lbl = QLabel("Pronto")
        self.status_lbl.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 10px;")
        self.status_lbl.setTextFormat(Qt.TextFormat.RichText)

        self.update_btn = ModernButton(
            "AGGIORNA DATABASE",
            variant=ModernButton.Variant.PRIMARY,
            size=ModernButton.Size.SMALL,
            icon=get_asset_path(Icons.REFRESH),
        )
        self.update_btn.clicked.connect(self.start_import_process)

        btn_h = QHBoxLayout()
        btn_h.setSpacing(5)
        btn_h.addWidget(self.update_btn)

        info_v.addWidget(self.status_lbl)
        info_v.addLayout(btn_h)
        toolbar_layout.addLayout(info_v)

        layout.addWidget(self.toolbar_card)

        self.main_tabs = AnimatedTabWidget()
        self.main_tabs.currentChanged.connect(self._on_main_tab_changed)

        self.year_tabs_widget = AnimatedTabWidget()
        self.year_tabs_widget.setTabPosition(QTabWidget.TabPosition.North)
        self.year_tabs_widget.currentChanged.connect(self._on_tab_changed)
        self.main_tabs.addTab(
            self.year_tabs_widget,
            get_colored_icon(get_asset_path(Icons.FOLDER), COLORS["text_muted"]),
            "Preventivi",
        )

        self.giornaliere_tabs_widget = AnimatedTabWidget()
        self.giornaliere_tabs_widget.setTabPosition(QTabWidget.TabPosition.North)
        self.giornaliere_tabs_widget.currentChanged.connect(self._on_tab_changed)
        self.main_tabs.addTab(
            self.giornaliere_tabs_widget,
            get_colored_icon(get_asset_path(Icons.FOLDER), COLORS["text_muted"]),
            "Giornaliere",
        )

        # Coda per inizializzazione differita tab pesanti
        self._init_queue = []
        self._tabs_initialized = False
        self.attivita_widget = None
        self.certificati_widget = None
        self.kpi_panel = None

        layout.addWidget(self.main_tabs)
        QTimer.singleShot(500, self._start_granular_init)

    def _start_granular_init(self) -> None:
        """Inizia la creazione dei tab pesanti in background."""
        from src.gui.widgets.contabilita.attivita_tab import AttivitaProgrammateTab
        from src.gui.widgets.contabilita.certificati_tab import CertificatiCampioneTab
        from src.gui.panels.contabilita_kpi import ContabilitaKPIPanel

        self._init_queue = [
            (AttivitaProgrammateTab, Icons.CALENDAR, "Attività Programmate", "attivita_widget"),
            (CertificatiCampioneTab, Icons.FILE_TEXT, "Certificati Campione", "certificati_widget"),
            (ContabilitaKPIPanel, Icons.BAR_CHART, "Analisi KPI", "kpi_panel"),
        ]
        self._process_init_queue()

    def _process_init_queue(self) -> None:
        """Crea un tab pesante alla volta, permettendo allo splash screen di respirare."""
        if not self._init_queue:
            self._tabs_initialized = True
            self.refresh_tabs()
            return

        cls, icon, label, attr_name = self._init_queue.pop(0)
        try:
            widget = cls()
            setattr(self, attr_name, widget)
            self.main_tabs.addTab(
                widget,
                get_colored_icon(get_asset_path(icon), COLORS["text_muted"]),
                label
            )
        except Exception as e:
            print(f"Errore caricamento tab contabilità {label}: {e}")

        # Passa al prossimo tab nel prossimo frame UI
        QTimer.singleShot(10, self._process_init_queue)

    def _on_search_changed(self, text: str) -> None:
        """Inoltra la stringa di ricerca al widget o al tab attualmente attivo."""
        current_widget = self.main_tabs.currentWidget()
        if isinstance(current_widget, (QTabWidget, AnimatedTabWidget)):
            current_widget = current_widget.currentWidget()
        if current_widget and hasattr(current_widget, "filter_data"):
            current_widget.filter_data(text)

    def _get_subtab_style(self) -> str:
        """Restituisce il QSS per i tab secondari posizionati in basso."""
        return f"""
            QTabWidget::pane {{ border: none; border-top: 1px solid {COLORS["border_light"]}; }}
            QTabBar::tab {{
                background: transparent; color: {COLORS["text_muted"]}; padding: 6px 16px; margin-bottom: -1px;
                border-bottom: 2px solid transparent; font-size: 13px; font-weight: 600;
            }}
            QTabBar::tab:selected {{ color: {COLORS["teal_accent"]}; border-bottom: 2px solid {COLORS["teal_accent"]}; background-color: {COLORS["bg_light"]}; }}
        """

    def _on_main_tab_changed(self, index: int) -> None:
        """Nasconde o mostra gli strumenti di ricerca in base al tab selezionato."""
        tab_text = self.main_tabs.tabText(index)
        is_kpi = "Analisi KPI" in tab_text
        self.toolbar_card.setVisible(not is_kpi)

        if not is_kpi:
            self._connect_selection_signal()
            text = self.search_input.text()
            if text:
                self._on_search_changed(text)
            self.search_input.setFocus()

    def refresh_tabs(self) -> None:
        """
        Interroga il database per gli anni disponibili e aggiorna i tab degli anni.
        Sincronizza inoltre i dati per le attività e i certificati.
        """
        years = ContabilitaManager.get_available_years()
        if not years:
            for tw in (self.year_tabs_widget, self.giornaliere_tabs_widget):
                tw.clear()
                tw.addTab(QLabel("Nessun dato disponibile."), "Info")
            return

        self._sync_tab_widget(self.year_tabs_widget, years, ContabilitaYearTab)
        self._sync_tab_widget(self.giornaliere_tabs_widget, years, GiornaliereYearTab)
        self._connect_selection_signal()

        if hasattr(self.kpi_panel, "refresh_years"):
            self.kpi_panel.refresh_years()

        if hasattr(self.attivita_widget, "refresh_data"):
            self.attivita_widget.refresh_data()

        if hasattr(self.certificati_widget, "refresh_data"):
            self.certificati_widget.refresh_data()

    def _sync_tab_widget(
        self, tab_widget: AnimatedTabWidget, target_years: list[int], tab_class: type
    ) -> None:
        """Aggiorna i tab di un AnimatedTabWidget senza distruggere i widget esistenti per gli stessi anni."""
        existing_years = {}
        for i in range(tab_widget.count()):
            with suppress(ValueError):
                existing_years[int(tab_widget.tabText(i))] = i

        for year in list(existing_years.keys()):
            if year not in target_years:
                tab_widget.removeTab(existing_years[year])
                self._sync_tab_widget(tab_widget, target_years, tab_class)
                return

        for year in target_years:
            if year in existing_years:
                widget = tab_widget.widget(existing_years[year])
                if widget and hasattr(widget, "refresh_data"):
                    widget.refresh_data()
            else:
                tab_widget.addTab(tab_class(year), str(year))

    def set_search_query(self, query: str) -> None:
        """Programma l'input di ricerca esternamente (es. da Quick Actions)."""
        self.search_input.setText(query)
        self.search_input.setFocus()
        self.search_input.selectAll()

    def _on_tab_changed(self, index: int) -> None:
        """Gestisce il cambio dell'anno all'interno di una categoria contabile."""
        self._connect_selection_signal()
        text = self.search_input.text()
        if text:
            self._on_search_changed(text)

    def _connect_selection_signal(self) -> None:
        """Collega dinamicamente i segnali di selezione della tabella attiva per aggiornare i totali ore."""
        curr = self.main_tabs.currentWidget()
        target = curr.currentWidget() if isinstance(curr, (QTabWidget, AnimatedTabWidget)) else curr

        if target:
            if hasattr(target, "table"):
                table = target.table
                if model := table.selectionModel():
                    with suppress(Exception):
                        model.selectionChanged.disconnect()
                    model.selectionChanged.connect(lambda s, d: self._update_selection_total(table))
            elif hasattr(target, "tree"):
                tree = target.tree
                with suppress(Exception):
                    tree.itemSelectionChanged.disconnect()
                tree.itemSelectionChanged.connect(lambda: self._update_selection_total(tree))

    def _update_selection_total(self, widget: QWidget) -> None:
        """Esegue il calcolo granulare delle ore selezionate filtrando le righe nascoste."""
        with suppress(Exception):
            if isinstance(widget, QTreeWidget):
                self.selection_count_label.setText(str(len(widget.selectedItems())))
                self.selection_sum_label.setText("")
                return

            if not isinstance(widget, QTableWidget):
                return

            model = widget.selectionModel()
            if not model:
                return

            indexes = model.selectedIndexes()
            if not indexes:
                self.selection_count_label.setText("0")
                self.selection_sum_label.setText("0")
                return

            target_col = self._find_ore_column(widget)
            selected_rows, total_ore = set(), 0.0
            for idx in indexes:
                row = idx.row()
                item_0 = widget.item(row, 0)
                is_total_row = item_0 and item_0.text() == "TOTALI"
                if not widget.isRowHidden(row) and not is_total_row:
                    selected_rows.add(row)

            if target_col != -1:
                for row in selected_rows:
                    if it := widget.item(row, target_col):
                        with suppress(Exception):
                            clean = str(it.text()).replace(".", "").replace(",", ".").strip()
                            if clean:
                                total_ore += float(clean)

            if total_ore % 1 != 0:
                fmt_ore = f"{total_ore:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            else:
                fmt_ore = str(int(total_ore))

            self.selection_count_label.setText(str(len(selected_rows)))
            self.selection_sum_label.setText(fmt_ore)

    def _find_ore_column(self, table: QTableWidget) -> int:
        """Individua l'indice della colonna contenente le ore in base all'header."""
        for c in range(table.columnCount()):
            h = table.horizontalHeaderItem(c)
            if h and ("ORE SP" in h.text().upper() or h.text().upper() == "ORE"):
                return c
        return -1

    def start_import_process(self) -> None:
        """Avvia il worker asincrono per l'importazione dei file Excel definiti nei path configurati."""
        config = config_manager.load_config()
        path = config.get("contabilita_file_path", "")
        if not path or not Path(path).exists():
            self.status_lbl.setText("File non trovato.")
            return

        self.update_btn.setDisabled(True)
        self.status_lbl.setText("Aggiornamento...")

        self.worker = ContabilitaWorker(
            path,
            config.get("giornaliere_path", ""),
            config.get("attivita_programmate_path", ""),
            config.get("certificati_campione_path", ""),
        )
        self.worker.finished_signal.connect(self._on_import_finished)
        self.worker.progress_signal.connect(self.status_lbl.setText)
        self.worker.start()

    def _on_import_finished(self, success: bool, msg: str, added: int, removed: int, duration: float) -> None:
        """Gestisce il completamento dell'importazione aggiornando lo stato e rinfrescando i dati."""
        if success:
            timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
            added_str = f"<font color='{COLORS['success_dark']}'><b>+{added}</b></font>"
            removed_str = f"<font color='{COLORS['error_red']}'><b>-{removed}</b></font>"
            if duration < 60:
                time_str = f"{duration:.1f}s"
            else:
                time_str = f"{int(duration // 60)}m {int(duration % 60)}s"
            final_status = f"{timestamp} {added_str} {removed_str} (Tempo: {time_str})"
            self._last_status_html = final_status
            self.status_lbl.setText(final_status)
            self.refresh_tabs()
        else:
            self.status_lbl.setText("Errore")
            ConfirmationDialog.show_error(self, "Errore", msg)
        self.worker = None
        self.update_btn.setDisabled(False)
