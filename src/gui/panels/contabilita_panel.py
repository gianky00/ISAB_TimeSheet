"""
Bot TS - Contabilita Panel
Pannello per la visualizzazione della Contabilità Strumentale.
"""

from contextlib import suppress
from datetime import datetime
from pathlib import Path

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
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
from src.gui.widgets.contabilita.attivita_tab import AttivitaProgrammateTab
from src.gui.widgets.contabilita.certificati_tab import CertificatiCampioneTab
from src.gui.widgets.contabilita.giornaliere_tab import GiornaliereYearTab
from src.gui.widgets.contabilita.year_tab import ContabilitaYearTab
from src.gui.widgets.modern_button import ModernButton
from src.utils.helpers import get_asset_path, get_colored_icon


class ContabilitaPanel(QWidget):
    """Pannello principale Strumentale."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.worker = None
        self.status_labels = []
        self.update_buttons = []
        self._last_status_html = "Pronto"
        self._setup_ui()
        # Defer heavy loading
        QTimer.singleShot(10, self._safe_refresh_tabs)

    def _safe_refresh_tabs(self):
        """Esegue il refresh dei tab in modo sicuro catturando eventuali eccezioni."""
        try:
            self.refresh_tabs()
        except Exception as e:
            import traceback

            print(f"❌ Error refreshing tabs for ContabilitaPanel: {e}")
            traceback.print_exc()

    def _setup_ui(self):
        """Inizializza l'interfaccia grafica del pannello contabilità."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)

        self.main_tabs = QTabWidget()
        self.main_tabs.setProperty("class", "Level2Tabs")  # Clean Line Style
        self.main_tabs.currentChanged.connect(self._on_main_tab_changed)

        # --- UNIFIED TOOLBAR (Corner Widget) ---
        self.toolbar_container = QWidget()
        toolbar_layout = QHBoxLayout(self.toolbar_container)
        toolbar_layout.setContentsMargins(0, 0, 0, 0)
        toolbar_layout.setSpacing(10)

        # Totali Selezione
        self.selection_count_label = QLabel("Righe: 0")
        self.selection_count_label.setStyleSheet("color: #607D8B; font-weight: 600; font-size: 12px;")
        self.selection_sum_label = QLabel("Totale ORE: 0")
        self.selection_sum_label.setStyleSheet("color: #009688; font-weight: 700; font-size: 12px;")

        # Search Input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Cerca nei dati...")
        self.search_input.setClearButtonEnabled(True)
        self.search_input.setFixedWidth(250)
        self.search_input.textChanged.connect(self._on_search_changed)

        # Status Label
        self.status_lbl = QLabel("Pronto")
        self.status_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_lbl.setStyleSheet("font-size: 12px;")
        self.status_lbl.setTextFormat(Qt.TextFormat.RichText)

        # Update Button
        self.update_btn = ModernButton(
            "Aggiorna",
            variant=ModernButton.Variant.PRIMARY,
            icon=get_asset_path(Icons.REFRESH),
        )
        self.update_btn.clicked.connect(self.start_import_process)

        toolbar_layout.addWidget(self.selection_count_label)
        toolbar_layout.addSpacing(10)
        toolbar_layout.addWidget(self.selection_sum_label)
        toolbar_layout.addSpacing(20)
        toolbar_layout.addWidget(self.search_input)
        toolbar_layout.addWidget(self.status_lbl)
        toolbar_layout.addWidget(self.update_btn)

        self.main_tabs.setCornerWidget(self.toolbar_container, Qt.Corner.TopRightCorner)

        # --- TABS ---

        # 1. Preventivi
        self.year_tabs_widget = QTabWidget()
        self.year_tabs_widget.setTabPosition(QTabWidget.TabPosition.South)
        self.year_tabs_widget.setStyleSheet(self._get_subtab_style())
        self.year_tabs_widget.currentChanged.connect(self._on_tab_changed)
        self.main_tabs.addTab(
            self.year_tabs_widget,
            get_colored_icon(get_asset_path(Icons.FOLDER), "#546E7A"),
            "Preventivi",
        )

        # 2. Giornaliere
        self.giornaliere_tabs_widget = QTabWidget()
        self.giornaliere_tabs_widget.setTabPosition(QTabWidget.TabPosition.South)
        self.giornaliere_tabs_widget.setStyleSheet(self._get_subtab_style())
        self.giornaliere_tabs_widget.currentChanged.connect(self._on_tab_changed)
        self.main_tabs.addTab(
            self.giornaliere_tabs_widget,
            get_colored_icon(get_asset_path(Icons.FOLDER), "#546E7A"),
            "Giornaliere",
        )

        # 3. Attività
        self.attivita_widget = AttivitaProgrammateTab()
        self.main_tabs.addTab(
            self.attivita_widget,
            get_colored_icon(get_asset_path(Icons.CALENDAR), "#546E7A"),
            "Attività Programmate",
        )

        # 4. Certificati
        self.certificati_widget = CertificatiCampioneTab()
        self.main_tabs.addTab(
            self.certificati_widget,
            get_colored_icon(get_asset_path(Icons.FILE_TEXT), "#546E7A"),
            "Certificati Campione",
        )

        # Lazy load per evitare circolarità
        from src.gui.panels.contabilita_kpi import ContabilitaKPIPanel

        self.kpi_panel = ContabilitaKPIPanel()
        self.main_tabs.addTab(
            self.kpi_panel,
            get_colored_icon(get_asset_path(Icons.BAR_CHART), "#546E7A"),
            "Analisi KPI",
        )

        layout.addWidget(self.main_tabs)

    def _on_search_changed(self, text):
        """Applica il filtro al widget attualmente visibile."""
        current_widget = self.main_tabs.currentWidget()

        # Se è un TabWidget (Preventivi/Giornaliere), prendi il tab interno corrente (Anno)
        if isinstance(current_widget, QTabWidget):
            current_widget = current_widget.currentWidget()

        if hasattr(current_widget, "filter_data"):
            current_widget.filter_data(text)

    def _proxy_filter(self, widget, text):
        # Deprecato ma mantenuto se servisse logica complessa
        pass

    def _get_subtab_style(self):
        """Restituisce il foglio di stile per i tab secondari (anni)."""
        return """
            QTabWidget::pane { border: none; border-top: 1px solid #E0E0E0; }
            QTabBar::tab {
                background: transparent;
                color: #78909C;
                padding: 6px 16px;
                margin-bottom: -1px;
                border-bottom: 2px solid transparent;
                font-size: 13px;
                font-weight: 600;
            }
            QTabBar::tab:selected {
                color: #009688;
                border-bottom: 2px solid #009688;
                background-color: #FAFAFA;
            }
            QTabBar::tab:hover:!selected {
                color: #00796B;
            }
        """

    def _on_main_tab_changed(self, index):
        """Gestisce il cambio del tab principale."""
        if "Analisi KPI" in self.main_tabs.tabText(index):
            self.selection_count_label.hide()
            self.selection_sum_label.hide()
            self.search_input.hide()
        else:
            self.selection_count_label.show()
            self.selection_sum_label.show()
            self.search_input.show()
            self._connect_selection_signal()

            # Applica il filtro corrente al nuovo tab (se presente)
            current_text = self.search_input.text()
            if current_text:
                self._on_search_changed(current_text)

        # Refocus ricerca
        if self.search_input.isVisible():
            self.search_input.setFocus()

    def refresh_tabs(self):
        """Aggiornamento incrementale dei tab per evitare flickering."""
        years = ContabilitaManager.get_available_years()
        if not years:
            self.year_tabs_widget.clear()
            self.giornaliere_tabs_widget.clear()
            no_data = QLabel("Nessun dato disponibile.")
            no_data.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.year_tabs_widget.addTab(no_data, "Info")
            return

        # --- Aggiornamento Tab Preventivi ---
        self._sync_tab_widget(self.year_tabs_widget, years, ContabilitaYearTab)

        # --- Aggiornamento Tab Giornaliere ---
        self._sync_tab_widget(self.giornaliere_tabs_widget, years, GiornaliereYearTab)

        self._connect_selection_signal()
        if hasattr(self, "kpi_panel"):
            self.kpi_panel.refresh_years()
        if hasattr(self, "attivita_widget"):
            self.attivita_widget.refresh_data()
        if hasattr(self, "certificati_widget"):
            self.certificati_widget.refresh_data()

    def _sync_tab_widget(self, tab_widget, target_years, tab_class):
        """Helper per sincronizzare gli anni nei tab senza distruggere tutto."""
        # 1. Trova anni attuali
        existing_years = {}
        for i in range(tab_widget.count()):
            try:
                year = int(tab_widget.tabText(i))
                existing_years[year] = i
            except ValueError:
                continue

        # 2. Rimuovi anni non più presenti
        for year in list(existing_years.keys()):
            if year not in target_years:
                tab_widget.removeTab(existing_years[year])
                # Ricalcola indici dopo rimozione
                return self._sync_tab_widget(tab_widget, target_years, tab_class)

        # 3. Aggiungi nuovi anni o rinfresca esistenti
        for year in target_years:
            if year in existing_years:
                # Già presente, rinfresca dati
                widget = tab_widget.widget(existing_years[year])
                if hasattr(widget, "refresh_data"):
                    widget.refresh_data()
            else:
                # Nuovo anno, aggiungi tab
                tab_widget.addTab(tab_class(year), str(year))
        return None

    def set_search_query(self, query):
        """Imposta il testo di ricerca nel tab corrente."""
        self.search_input.setText(query)
        self.search_input.setFocus()
        self.search_input.selectAll()

    def _on_tab_changed(self, index):
        """Gestisce il cambio di un tab secondario."""
        self._connect_selection_signal()
        # Riapplica filtro se c'è testo
        if self.search_input.text():
            self._on_search_changed(self.search_input.text())

    def _connect_selection_signal(self):
        """Collega i segnali di selezione della tabella/albero per il calcolo dei totali."""
        curr = self.main_tabs.currentWidget()
        target = None
        if curr == self.year_tabs_widget:  # Preventivi
            target = self.year_tabs_widget.currentWidget()
        elif curr == self.giornaliere_tabs_widget:  # Giornaliere
            target = self.giornaliere_tabs_widget.currentWidget()
        elif curr == self.attivita_widget:
            target = self.attivita_widget
        elif curr == self.certificati_widget:
            target = self.certificati_widget

        if target:
            if hasattr(target, "table"):
                with suppress(Exception):
                    target.table.selectionModel().selectionChanged.disconnect()
                target.table.selectionModel().selectionChanged.connect(
                    lambda s, d: self._update_selection_total(target.table)
                )
            elif hasattr(target, "tree"):
                with suppress(Exception):
                    target.tree.itemSelectionChanged.disconnect()
                target.tree.itemSelectionChanged.connect(lambda: self._update_selection_total(target.tree))

    def _update_selection_total(self, widget):
        """Calcola e visualizza i totali per le righe selezionate (Table o Tree)."""
        with suppress(Exception):
            if isinstance(widget, QTreeWidget):
                self._handle_tree_selection(widget)
                return

            indexes = widget.selectionModel().selectedIndexes()
            if not indexes:
                self.selection_count_label.setText("Righe: 0")
                self.selection_sum_label.setText("Totale ORE: 0")
                return

            target_col = self._find_ore_column(widget)
            selected_rows, total_ore = self._calculate_selection_stats(widget, indexes, target_col)

            fmt_ore = self._format_ore_display(total_ore)
            self.selection_count_label.setText(f"Righe: {len(selected_rows)}")
            self.selection_sum_label.setText(f"Totale ORE: {fmt_ore}")

    def _handle_tree_selection(self, tree: QTreeWidget):
        self.selection_count_label.setText(f"Selezionati: {len(tree.selectedItems())}")
        self.selection_sum_label.setText("")

    def _find_ore_column(self, table: QTableWidget) -> int:
        for c in range(table.columnCount()):
            h = table.horizontalHeaderItem(c)
            if h and ("ORE SP" in h.text().upper() or h.text().upper() == "ORE"):
                return c
        return -1

    def _calculate_selection_stats(self, widget, indexes, target_col) -> tuple[set[int], float]:
        selected_rows, total_ore = set(), 0.0
        for idx in indexes:
            row = idx.row()
            if widget.isRowHidden(row) or (widget.item(row, 0) and widget.item(row, 0).text() == "TOTALI"):
                continue
            selected_rows.add(row)

        if target_col != -1:
            for row in selected_rows:
                it = widget.item(row, target_col)
                if it:
                    with suppress(Exception):
                        clean = str(it.text()).replace(".", "").replace(",", ".").strip()
                        if clean:
                            total_ore += float(clean)
        return selected_rows, total_ore

    def _format_ore_display(self, total: float) -> str:
        if total % 1 == 0:
            return str(int(total))
        return f"{total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def start_import_process(self):
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

    def _update_all_status_labels(self, text):
        # Legacy compat
        self.status_lbl.setText(text)

    def _on_import_finished(self, success, msg, added, removed, duration):
        if success:
            timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
            added_str = f"<font color='green'><b>+{added}</b></font>"
            removed_str = f"<font color='red'><b>-{removed}</b></font>"

            if duration < 60:
                time_str = f"{duration:.1f}s"
            else:
                m, s = divmod(int(duration), 60)
                time_str = f"{m}m {s}s"

            final_status = f"{timestamp} {added_str} {removed_str} (Tempo: {time_str})"
            self._last_status_html = final_status
            self.status_lbl.setText(final_status)
            self.refresh_tabs()
        else:
            self.status_lbl.setText("Errore")
            QMessageBox.warning(self, "Errore", msg)
        self.worker = None
        self.update_btn.setDisabled(False)
