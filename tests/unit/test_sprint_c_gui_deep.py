import pytest
from PyQt6.QtWidgets import (
    QApplication,
    QTableWidget,
    QTableWidgetItem,
)

from src.gui.panels.contabilita_kpi.kpi_panel import ContabilitaKPIPanel
from src.gui.panels.contabilita_panel import ContabilitaPanel


class TestSprintCGUIDeep:
    @pytest.fixture
    def panel(self, qapp, mocker):
        # Mocking heavy managers
        mocker.patch(
            "src.core.contabilita_manager.ContabilitaManager.get_available_years",
            return_value=[2023, 2024],
        )
        mocker.patch(
            "src.core.contabilita_manager.ContabilitaManager.get_year_stats",
            return_value={
                "total_prev": 1000.0,
                "total_ore": 50.0,
                "count_total": 5,
                "ore_dirette": 40.0,
                "ore_indirette": 10.0,
            },
        )
        mocker.patch(
            "src.core.contabilita_manager.ContabilitaManager.get_data_by_year",
            return_value=[],
        )

        # Mocking matplotlib
        mocker.patch("matplotlib.figure.Figure.add_subplot")
        mocker.patch("matplotlib.backends.backend_qtagg.FigureCanvasQTAgg.draw")

        p = ContabilitaPanel()
        # Forziamo il caricamento immediato (bypass timer)
        p.refresh_tabs()
        return p

    def test_contabilita_tab_synchronization(self, panel, qapp, mocker):
        """Verifica la creazione dinamica dei tab annuali."""
        QApplication.processEvents()

        # Tab Preventivi
        tabs = panel.year_tabs_widget
        texts = [tabs.tabText(i) for i in range(tabs.count())]
        assert "2023" in texts
        assert "2024" in texts

        # Update: rimuovi uno, aggiungi uno
        mocker.patch(
            "src.core.contabilita_manager.ContabilitaManager.get_available_years",
            return_value=[2024, 2025],
        )
        panel.refresh_tabs()
        QApplication.processEvents()

        new_texts = [tabs.tabText(i) for i in range(tabs.count())]
        assert "2023" not in new_texts
        assert "2025" in new_texts

    def test_kpi_card_formatting(self, qapp, mocker):
        """Verifica che le card KPI formattino correttamente i valori."""
        mocker.patch(
            "src.core.contabilita_manager.ContabilitaManager.get_available_years",
            return_value=[2024],
        )
        mocker.patch(
            "src.core.contabilita_manager.ContabilitaManager.get_year_stats",
            return_value={
                "total_prev": 1500.50,
                "total_ore": 10.0,
                "count_total": 1,
                "ore_dirette": 10.0,
                "ore_indirette": 0.0,
            },
        )

        # Mock plotting (ora in KPIChartsManager tramite charts_manager)
        from src.gui.panels.contabilita_kpi.charts import KPIChartsManager

        mocker.patch.object(KPIChartsManager, "_plot_stato_attivita")
        mocker.patch.object(KPIChartsManager, "_plot_prev_ore_mese")
        mocker.patch.object(KPIChartsManager, "_plot_margine_tipologia")
        mocker.patch.object(KPIChartsManager, "_plot_andamento_resa")
        mocker.patch.object(KPIChartsManager, "_plot_completamento")

        kpi = ContabilitaKPIPanel()
        QApplication.processEvents()

        val_text = kpi.card_totale.lbl_value.text()
        assert "1.500,50" in val_text

    def test_selection_sum_calculation(self, panel, qapp):
        """Verifica la somma automatica delle ore selezionate."""
        # 1. Setup tabella reale con dati
        table = QTableWidget(3, 10)
        table.setHorizontalHeaderLabels(["", "", "", "", "", "", "", "", "", "ORE SP"])
        table.setItem(0, 9, QTableWidgetItem("10,0"))
        table.setItem(1, 9, QTableWidgetItem("5,5"))
        table.setItem(2, 9, QTableWidgetItem("1,0"))

        # 2. Inseriamo la tabella nel pannello simulando il widget attivo
        # Non possiamo iniettarla facilmente nei tab dinamici, testiamo il metodo di calcolo direttamente
        panel._update_selection_total(table)  # Vuoto
        assert "Righe: 0" in panel.selection_count_label.text()

        # 3. Selezioniamo le prime due righe
        table.selectRow(0)
        from PyQt6.QtWidgets import QTableWidgetSelectionRange

        table.setRangeSelected(QTableWidgetSelectionRange(0, 0, 0, 9), True)
        # Per semplicità nei test headless forziamo la selezione manuale nel modello
        table.selectAll()

        panel._update_selection_total(table)

        # 10 + 5,5 + 1 = 16,5
        assert "16,5" in panel.selection_sum_label.text()
        assert "Righe: 3" in panel.selection_count_label.text()

    def test_search_filtering_proxy(self, panel, qapp, mocker):
        """Verifica che la ricerca superiore deleghi al tab corrente."""
        # Seleziona il tab Attività Programmate
        panel.main_tabs.setCurrentWidget(panel.attivita_widget)
        mock_filter = mocker.patch.object(panel.attivita_widget, "filter_data")

        # La ricerca è globale nel pannello (search_input)
        panel.search_input.setText("SearchQuery")

        mock_filter.assert_called_with("SearchQuery")
