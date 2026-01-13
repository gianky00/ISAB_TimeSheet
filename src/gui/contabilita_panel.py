"""
Bot TS - Contabilita Panel
Pannello per la visualizzazione della Contabilità Strumentale.
"""

import os
from datetime import datetime

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTabWidget,
    QTreeWidget,
    QVBoxLayout,
    QWidget,
)

from src.core import config_manager
from src.core.contabilita_manager import ContabilitaManager
from src.core.contabilita_worker import ContabilitaWorker
from src.gui.widgets.contabilita.attivita_tab import AttivitaProgrammateTab
from src.gui.widgets.contabilita.certificati_tab import CertificatiCampioneTab
from src.gui.widgets.contabilita.giornaliere_tab import GiornaliereYearTab
from src.gui.widgets.contabilita.year_tab import ContabilitaYearTab


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
        try:
            self.refresh_tabs()
        except Exception as e:
            import traceback
            print(f"❌ Error refreshing tabs for ContabilitaPanel: {e}")
            traceback.print_exc()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)

        self.main_tabs = QTabWidget()
        self.main_tabs.currentChanged.connect(self._on_main_tab_changed)
        self.main_tabs.setStyleSheet("""
            QTabWidget::pane { border: 1px solid #dee2e6; border-radius: 6px; background-color: white; }
            QTabBar::tab { background: #f8f9fa; border: 1px solid #dee2e6; padding: 10px 20px; margin-right: 2px; border-top-left-radius: 6px; border-top-right-radius: 6px; color: #495057; font-weight: bold; font-size: 14px; }
            QTabBar::tab:selected { background: white; border-bottom-color: white; color: #0d6efd; }
        """)

        self.selection_container = QWidget()
        selection_layout = QHBoxLayout(self.selection_container)
        selection_layout.setContentsMargins(0, 0, 10, 0)
        selection_layout.setSpacing(15)
        self.selection_count_label = QLabel("Righe: 0")
        self.selection_count_label.setStyleSheet("color: #6c757d; font-weight: bold;")
        self.selection_sum_label = QLabel("Totale ORE SP: 0")
        self.selection_sum_label.setStyleSheet("color: #0d6efd; font-weight: bold;")
        selection_layout.addWidget(self.selection_count_label)
        selection_layout.addWidget(self.selection_sum_label)
        self.main_tabs.setCornerWidget(
            self.selection_container, Qt.Corner.TopRightCorner
        )

        self.year_tabs_widget = QTabWidget()
        self.year_tabs_widget.setTabPosition(QTabWidget.TabPosition.South)
        self.year_tabs_widget.setStyleSheet(self._get_subtab_style())
        self.year_tabs_widget.currentChanged.connect(self._on_tab_changed)
        self.tab_preventivi = self._create_tab_wrapper(
            self.year_tabs_widget, "🔍 Cerca preventivi..."
        )
        self.main_tabs.addTab(self.tab_preventivi, "📂 Preventivi")

        self.giornaliere_tabs_widget = QTabWidget()
        self.giornaliere_tabs_widget.setTabPosition(QTabWidget.TabPosition.South)
        self.giornaliere_tabs_widget.setStyleSheet(self._get_subtab_style())
        self.giornaliere_tabs_widget.currentChanged.connect(self._on_tab_changed)
        self.tab_giornaliere = self._create_tab_wrapper(
            self.giornaliere_tabs_widget, "🔍 Cerca giornaliere..."
        )
        self.main_tabs.addTab(self.tab_giornaliere, "📂 Giornaliere")

        self.attivita_widget = AttivitaProgrammateTab()
        self.tab_attivita = self._create_tab_wrapper(
            self.attivita_widget, "🔍 Cerca attività..."
        )
        self.main_tabs.addTab(self.tab_attivita, "📅 Attività Programmate")

        self.certificati_widget = CertificatiCampioneTab()
        self.tab_certificati = self._create_tab_wrapper(
            self.certificati_widget, "🔍 Cerca certificati..."
        )
        self.main_tabs.addTab(self.tab_certificati, "📜 Certificati Campione")

        from src.gui.contabilita_kpi_panel import ContabilitaKPIPanel

        self.kpi_panel = ContabilitaKPIPanel()
        self.main_tabs.addTab(self.kpi_panel, "📊 Analisi KPI")
        layout.addWidget(self.main_tabs)

    def _create_tab_wrapper(self, content_widget, placeholder_text):
        wrapper = QWidget()
        layout = QVBoxLayout(wrapper)
        layout.setContentsMargins(10, 10, 10, 10)
        toolbar = QHBoxLayout()
        search_input = QLineEdit()
        search_input.setPlaceholderText(placeholder_text)
        search_input.setClearButtonEnabled(True)
        search_input.setFixedWidth(400)
        search_input.setStyleSheet(
            "QLineEdit { border: 1px solid #ced4da; border-radius: 4px; padding: 6px 12px; font-size: 14px; background-color: white; color: black; } QLineEdit:focus { border-color: #0d6efd; }"
        )
        search_input.textChanged.connect(
            lambda t: self._proxy_filter(content_widget, t)
        )
        if isinstance(content_widget, QTabWidget):
            content_widget.currentChanged.connect(
                lambda: self._proxy_filter(content_widget, search_input.text())
            )
        toolbar.addWidget(search_input)
        toolbar.addStretch()
        status_lbl = QLabel(self._last_status_html)
        status_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        status_lbl.setStyleSheet(
            "QLabel { color: #495057; font-size: 14px; font-weight: 500; padding: 5px 10px; background-color: #f8f9fa; border-radius: 4px; border: 1px solid #dee2e6; }"
        )
        self.status_labels.append(status_lbl)
        toolbar.addWidget(status_lbl)
        toolbar.addStretch()
        update_btn = QPushButton("🔄 Aggiorna Dati")
        update_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        update_btn.setStyleSheet(
            "QPushButton { background-color: #0d6efd; color: white; border: none; border-radius: 4px; padding: 6px 12px; font-weight: bold; font-size: 13px; } QPushButton:hover { background-color: #0b5ed7; }"
        )
        update_btn.clicked.connect(self.start_import_process)
        self.update_buttons.append(update_btn)
        toolbar.addWidget(update_btn)
        layout.addLayout(toolbar)
        layout.addWidget(content_widget)
        return wrapper

    def _proxy_filter(self, widget, text):
        target = widget.currentWidget() if isinstance(widget, QTabWidget) else widget
        if hasattr(target, "filter_data"):
            target.filter_data(text)

    def _get_subtab_style(self):
        return "QTabWidget::pane { border: none; } QTabBar::tab { background: #f1f3f5; padding: 6px 15px; margin-right: 2px; border-top-left-radius: 4px; border-top-right-radius: 4px; font-size: 13px; } QTabBar::tab:selected { background: #0d6efd; color: white; }"

    def _on_main_tab_changed(self, index):
        if "Analisi KPI" in self.main_tabs.tabText(index):
            self.selection_container.hide()
        else:
            self.selection_container.show()
            self._connect_selection_signal()

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

    def set_search_query(self, query):
        search_edit = self.main_tabs.currentWidget().findChild(QLineEdit)
        if search_edit:
            search_edit.setText(query)
            search_edit.setFocus()
            search_edit.selectAll()

    def _on_tab_changed(self, index):
        self._connect_selection_signal()

    def _connect_selection_signal(self):
        curr = self.main_tabs.currentWidget()
        target = None
        if curr == self.tab_preventivi:
            target = self.year_tabs_widget.currentWidget()
        elif curr == self.tab_giornaliere:
            target = self.giornaliere_tabs_widget.currentWidget()
        elif curr == self.tab_attivita:
            target = self.attivita_widget
        elif curr == self.tab_certificati:
            target = self.certificati_widget

        if target:
            if hasattr(target, "table"):
                try:
                    target.table.selectionModel().selectionChanged.disconnect()
                except Exception:
                    pass
                target.table.selectionModel().selectionChanged.connect(
                    lambda s, d: self._update_selection_total(target.table)
                )
            elif hasattr(target, "tree"):
                try:
                    target.tree.itemSelectionChanged.disconnect()
                except Exception:
                    pass
                target.tree.itemSelectionChanged.connect(
                    lambda: self._update_selection_total(target.tree)
                )

    def _update_selection_total(self, widget):
        """Calcola e visualizza i totali per le righe selezionate (Table o Tree)."""
        try:
            if isinstance(widget, QTreeWidget):
                self._handle_tree_selection(widget)
                return

            indexes = widget.selectionModel().selectedIndexes()
            if not indexes:
                self.selection_count_label.setText("Righe: 0")
                self.selection_sum_label.setText("Totale ORE SP: 0")
                return

            target_col = self._find_ore_column(widget)
            selected_rows, total_ore = self._calculate_selection_stats(widget, indexes, target_col)

            fmt_ore = self._format_ore_display(total_ore)
            self.selection_count_label.setText(f"Righe: {len(selected_rows)}")
            self.selection_sum_label.setText(f"Totale ORE SP: {fmt_ore}")
        except Exception:
            pass

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
                    try:
                        clean = str(it.text()).replace(".", "").replace(",", ".").strip()
                        if clean:
                            total_ore += float(clean)
                    except Exception:
                        pass
        return selected_rows, total_ore

    def _format_ore_display(self, total: float) -> str:
        if total % 1 == 0:
            return str(int(total))
        return f"{total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def start_import_process(self):
        config = config_manager.load_config()
        path = config.get("contabilita_file_path", "")
        if not path or not os.path.exists(path):
            for lbl in self.status_labels:
                lbl.setText("⚠️ File non trovato.")
            return
        for btn in self.update_buttons:
            btn.setDisabled(True)
        for lbl in self.status_labels:
            lbl.setText("🔄 Aggiornamento...")
        self.worker = ContabilitaWorker(
            path,
            config.get("giornaliere_path", ""),
            config.get("attivita_programmate_path", ""),
            config.get("certificati_campione_path", ""),
        )
        self.worker.finished_signal.connect(self._on_import_finished)
        self.worker.progress_signal.connect(self._update_all_status_labels)
        self.worker.start()

    def _update_all_status_labels(self, text):
        for lbl in self.status_labels:
            lbl.setText(text)

    def _on_import_finished(self, success, msg, added, removed, duration):
        if success:
            now = datetime.now().strftime("%d/%m/%Y %H:%M")
            time_str = (
                f"{duration:.1f}s"
                if duration < 60
                else f"{int(duration // 60)}m {int(duration % 60)}s"
            )
            status = f"✅ {now} <font color='green'><b>+{added}</b></font> <font color='red'><b>-{removed}</b></font> ({time_str})"
            self._last_status_html = status
            for lbl in self.status_labels:
                lbl.setText(status)
            self.refresh_tabs()
        else:
            for lbl in self.status_labels:
                lbl.setText(f"❌ Errore: {msg}")
            QMessageBox.warning(self, "Errore", msg)
        self.worker = None
        for btn in self.update_buttons:
            btn.setDisabled(False)
