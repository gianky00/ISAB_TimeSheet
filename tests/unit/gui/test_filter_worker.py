import pytest
from src.gui.components.scarico_ore.filter_worker import FilterWorker

def test_filter_worker_basic(qtbot):
    """Testa che il QThread esegua correttamente il filtraggio ed emetta il segnale finished."""
    # Arrange
    search_index = ["mario rossi isab", "luigi bianchi erg"]
    display_data = [["Mario Rossi", "ISAB"], ["Luigi Bianchi", "ERG"]]
    
    worker = FilterWorker(search_index, display_data, text="rossi")
    
    # Act & Assert
    # waitSignal blocca asincronamente fino all'emissione del segnale o al timeout
    with qtbot.waitSignal(worker.finished, timeout=2000) as blocker:
        worker.start()
        
    # Verifichiamo che il segnale sia stato emesso con i parametri corretti (lista_indici, count)
    assert blocker.args == [[0], 1], "Deve trovare solo l'indice 0 (Mario Rossi)"

def test_filter_worker_cancellation(qtbot):
    """Testa che la chiamata a cancel() interrompa il thread senza DB lock e prevenga segnali fantasma."""
    # Arrange (dataset grosso per dare tempo al thread di farsi cancellare)
    search_index = ["test string"] * 500000
    display_data = [["test", "string"]] * 500000
    worker = FilterWorker(search_index, display_data, text="test")
    
    # Act
    worker.start()
    worker.cancel() # Interruzione simulata utente (es. ha digitato un'altra lettera)
    
    # Assert
    # Attendiamo la chiusura del thread, ma ci aspettiamo che il segnale 'finished' NON venga emesso
    with qtbot.waitSignal(worker.finished, timeout=1000, raising=False) as blocker:
        pass
        
    assert not blocker.signal_triggered, "Il segnale finished non deve essere emesso se cancellato"
    assert worker._is_cancelled is True
    assert not worker.isRunning(), "Il worker deve essersi chiuso correttamente (no zombie threads)"
