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
from src.gui.components.animated_tab_widget import AnimatedTabWidget
from src.gui.widgets.contabilita.attivita_tab import AttivitaProgrammateTab
from src.gui.widgets.contabilita.certificati_tab import CertificatiCampioneTab
from src.gui.widgets.contabilita.giornaliere_tab import GiornaliereYearTab
from src.gui.widgets.contabilita.year_tab import ContabilitaYearTab
from src.gui.widgets.modern_button import ModernButton
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

        self.main_tabs = AnimatedTabWidget()
        # self.main_tabs.setProperty("class", "Level2Tabs") # Rimosso per ora, stile gestito internamente
        self.main_tabs.currentChanged.connect(self._on_main_tab_changed)

        # --- UNIFIED TOOLBAR ---
        self.toolbar_container = QWidget()
        toolbar_layout = QHBoxLayout(self.toolbar_container)
        toolbar_layout.setContentsMargins(0, 0, 0, 0)
        toolbar_layout.setSpacing(10)

        self.selection_count_label = QLabel("Righe: 0")
        self.selection_count_label.setStyleSheet("color: #607D8B; font-weight: 600; font-size: 12px;")
        self.selection_sum_label = QLabel("Totale ORE: 0")
        self.selection_sum_label.setStyleSheet("color: #009688; font-weight: 700; font-size: 12px;")

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Cerca nei dati...")
        self.search_input.setClearButtonEnabled(True)
        self.search_input.setFixedWidth(250)
        self.search_input.textChanged.connect(self._on_search_changed)

        self.status_lbl = QLabel("Pronto")
        self.status_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_lbl.setStyleSheet("font-size: 12px;")
        self.status_lbl.setTextFormat(Qt.TextFormat.RichText)

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

        layout.addWidget(self.toolbar_container)

        # --- TABS ---
        self.year_tabs_widget = AnimatedTabWidget()
        self.year_tabs_widget.setTabPosition(QTabWidget.TabPosition.North)
        # self.year_tabs_widget.setStyleSheet(self._get_subtab_style()) # Stile ora gestito internamente
        self.year_tabs_widget.currentChanged.connect(self._on_tab_changed)
        self.main_tabs.addTab(
            self.year_tabs_widget,
            get_colored_icon(get_asset_path(Icons.FOLDER), "#546E7A"),
            "Preventivi",
        )

        self.giornaliere_tabs_widget = AnimatedTabWidget()
        self.giornaliere_tabs_widget.setTabPosition(QTabWidget.TabPosition.North)
        # self.giornaliere_tabs_widget.setStyleSheet(self._get_subtab_style())
        self.giornaliere_tabs_widget.currentChanged.connect(self._on_tab_changed)
        self.main_tabs.addTab(
            self.giornaliere_tabs_widget,
            get_colored_icon(get_asset_path(Icons.FOLDER), "#546E7A"),
            "Giornaliere",
        )

        self.attivita_widget = AttivitaProgrammateTab()
        self.main_tabs.addTab(
            self.attivita_widget,
            get_colored_icon(get_asset_path(Icons.CALENDAR), "#546E7A"),
            "Attività Programmate",
        )

        self.certificati_widget = CertificatiCampioneTab()
        self.main_tabs.addTab(
            self.certificati_widget,
            get_colored_icon(get_asset_path(Icons.FILE_TEXT), "#546E7A"),
            "Certificati Campione",
        )

        from src.gui.panels.contabilita_kpi import ContabilitaKPIPanel

        self.kpi_panel = ContabilitaKPIPanel()
        self.main_tabs.addTab(
            self.kpi_panel,
            get_colored_icon(get_asset_path(Icons.BAR_CHART), "#546E7A"),
            "Analisi KPI",
        )

        layout.addWidget(self.main_tabs)

    def _on_search_changed(self, text: str) -> None:
        """Inoltra la stringa di ricerca al widget o al tab attualmente attivo."""
        current_widget = self.main_tabs.currentWidget()
        if isinstance(current_widget, (QTabWidget, AnimatedTabWidget)):
            current_widget = current_widget.currentWidget()
        if current_widget and hasattr(current_widget, "filter_data"):
            current_widget.filter_data(text)

    def _get_subtab_style(self) -> str:
        """Restituisce il QSS per i tab secondari posizionati in basso."""
        return """
            QTabWidget::pane { border: none; border-top: 1px solid #E0E0E0; }
            QTabBar::tab {
                background: transparent; color: #78909C; padding: 6px 16px; margin-bottom: -1px;
                border-bottom: 2px solid transparent; font-size: 13px; font-weight: 600;
            }
            QTabBar::tab:selected { color: #009688; border-bottom: 2px solid #009688; background-color: #FAFAFA; }
        """

    def _on_main_tab_changed(self, index: int) -> None:
        """Nasconde o mostra gli strumenti di ricerca in base al tab selezionato."""
        tab_text = self.main_tabs.tabText(index)
        is_kpi = "Analisi KPI" in tab_text
        self.selection_count_label.setVisible(not is_kpi)
        self.selection_sum_label.setVisible(not is_kpi)
        self.search_input.setVisible(not is_kpi)

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

    def _sync_tab_widget(self, tab_widget: QTabWidget, target_years: list[int], tab_class: type) -> None:
        """Aggiorna i tab di un QTabWidget senza distruggere i widget esistenti per gli stessi anni."""
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
                self.selection_count_label.setText(f"Selezionati: {len(widget.selectedItems())}")
                self.selection_sum_label.setText("")
                return

            if not isinstance(widget, QTableWidget):
                return

            model = widget.selectionModel()
            if not model:
                return

            indexes = model.selectedIndexes()
            if not indexes:
                self.selection_count_label.setText("Righe: 0")
                self.selection_sum_label.setText("Totale ORE: 0")
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

            self.selection_count_label.setText(f"Righe: {len(selected_rows)}")
            self.selection_sum_label.setText(f"Totale ORE: {fmt_ore}")

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
            added_str = f"<font color='green'><b>+{added}</b></font>"
            removed_str = f"<font color='red'><b>-{removed}</b></font>"
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
            QMessageBox.warning(self, "Errore", msg)
        self.worker = None
        self.update_btn.setDisabled(False)
