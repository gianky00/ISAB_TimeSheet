from PyQt6.QtWidgets import QLabel

from src.gui.widgets.timeline_widget import TimelineWidget


def test_timeline_functionality(qtbot):  # noqa: ANN001
    """Verifica l'aggiunta di log nella nuova TimelineWidget V9.0."""
    widget = TimelineWidget()
    qtbot.addWidget(widget)

    logs_to_add = [
        "🚀 Avvio sistema",
        "🔐 Login in corso...",
        "✅ Accesso effettuato",
    ]

    for log_message in logs_to_add:
        widget.add_log(log_message)

    # In V9.0 i log sono aggiunti a un layout verticale contenuto in una scroll area
    # Troviamo i QLabel creati
    labels = widget.findChildren(QLabel)

    # Verifichiamo che i testi siano presenti (filtrando eventuali placeholder)
    texts = [label.text() for label in labels]
    for log in logs_to_add:
        assert any(log in t for t in texts)


def test_timeline_autoscroll_safe(qtbot):  # noqa: ANN001
    """Verifica che l'aggiunta massiva di log non crashi (autoscroll safe)."""
    widget = TimelineWidget()
    qtbot.addWidget(widget)

    for i in range(100):
        widget.add_log(f"Log riga {i}")

    # Se arriviamo qui senza RuntimeError, il fix sip.isdeleted() sta funzionando
    assert True
