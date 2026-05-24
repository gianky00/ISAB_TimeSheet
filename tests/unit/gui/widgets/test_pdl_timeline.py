"""Unit tests for PDLTimelineWidget."""

import pytest
from PySide6.QtWidgets import QLabel

from src.gui.styles import COLORS
from src.gui.widgets.pdl_timeline import PDLTimelineWidget


@pytest.fixture
def timeline_data():
    """Dati di test per la timeline."""
    return [
        {
            "data": "2026-05-24",
            "tecnico": "Mario Rossi",
            "descrizione": "Installazione nuova PDL",
            "fonte": "Relazione Tecnica",
            "ore_lavoro": "4.5",
        },
        {
            "data": "10/05/2026",
            "tecnico": "Luigi Bianchi",
            "descrizione": "Manutenzione ordinaria",
            "fonte": "Validato",
            "ore_lavoro": "2",
        },
        {
            "data": "2026-05-15 09:00:00",
            "tecnico": "Gianni Verdi",
            "descrizione": "Controllo sicurezza",
            "fonte": "In Attesa",
            "ore_lavoro": "0",
        },
    ]


class TestPDLTimelineWidget:
    """Test suite per PDLTimelineWidget."""

    def test_empty_data(self, qtbot):
        """Verifica il comportamento con lista dati vuota."""
        widget = PDLTimelineWidget([])
        qtbot.addWidget(widget)

        # Dovrebbe esserci una label con il messaggio di fallback
        labels = widget.findChildren(QLabel)
        assert any("Nessuna attività registrata" in lbl.text() for lbl in labels)

    def test_data_sorting(self, qtbot, timeline_data):
        """Verifica che gli eventi siano ordinati per data decrescente."""
        widget = PDLTimelineWidget(timeline_data)
        qtbot.addWidget(widget)

        # 24/05/2026 deve essere il primo (indice 0)
        assert widget.data[0]["data"] == "2026-05-24"
        # 15/05/2026 (dal timestamp) deve essere il secondo
        assert "2026-05-15" in widget.data[1]["data"]
        # 10/05/2026 deve essere lbl'ultimo
        assert widget.data[2]["data"] == "10/05/2026"

    def test_date_parsing_formats(self, qtbot):
        """Verifica il parsing di diversi formati data."""
        data = [{"data": "2026-12-31"}, {"data": "01/01/2026"}]
        widget = PDLTimelineWidget(data)
        qtbot.addWidget(widget)

        # Primo evento (31 Dic)
        date_widget1 = widget._create_date_widget(widget.data[0])
        labels1 = date_widget1.findChildren(QLabel)
        assert any(lbl.text() == "31" for lbl in labels1)
        assert any(lbl.text() == "DEC" for lbl in labels1)

        # Secondo evento (01 Gen)
        date_widget2 = widget._create_date_widget(widget.data[1])
        labels2 = date_widget2.findChildren(QLabel)
        assert any(lbl.text() == "01" for lbl in labels2)
        assert any(lbl.text() == "JAN" for lbl in labels2)

    def test_status_and_badge_colors(self, qtbot):
        """Verifica la logica dei colori basata sulla fonte."""
        widget = PDLTimelineWidget([])
        qtbot.addWidget(widget)

        # Success/Validato
        assert widget._get_status_color("Validato") == COLORS["success_dark"]
        bg, _ = widget._get_badge_colors("Validato")
        assert bg == COLORS["success_dark"]

        # Warning/In Attesa
        assert widget._get_status_color("In Attesa") == COLORS["warning_orange"]
        bg, _ = widget._get_badge_colors("In Attesa")
        assert bg == COLORS["warning_yellow"]

        # Purple/Relazione
        assert widget._get_status_color("Relazione") == COLORS["purple"]
        bg, _ = widget._get_badge_colors("Relazione")
        assert bg == COLORS["purple"]

        # Default
        assert widget._get_status_color("Altro") == COLORS["text_muted"]

    def test_card_content_rendering(self, qtbot, timeline_data):
        """Verifica che i contenuti della card siano renderizzati."""
        widget = PDLTimelineWidget(timeline_data)
        qtbot.addWidget(widget)

        # Cerchiamo la card di Mario Rossi
        mario_card = None
        for i in range(widget.layout().count()):
            item = widget.layout().itemAt(i).widget()
            if item:
                labels = item.findChildren(QLabel)
                if any("Mario Rossi" in lbl.text() for lbl in labels):
                    mario_card = item
                    break

        assert mario_card is not None
        labels = mario_card.findChildren(QLabel)
        assert any("Installazione nuova PDL" in lbl.text() for lbl in labels)
        assert any("4.5 ore" in lbl.text() for lbl in labels)

        # Verifica che per "Gianni Verdi" (0 ore) non compaia la label delle ore
        gianni_card = None
        for i in range(widget.layout().count()):
            item = widget.layout().itemAt(i).widget()
            if item:
                labels = item.findChildren(QLabel)
                if any("Gianni Verdi" in lbl.text() for lbl in labels):
                    gianni_card = item
                    break

        assert gianni_card is not None
        gianni_labels = gianni_card.findChildren(QLabel)
        # Il testo "0 ore" non dovrebbe esserci
        assert not any("0 ore" in lbl.text() for lbl in gianni_labels)
