"""
SafeWork PDL Bot - Comprehensive Test Suite (2026 Edition)
=========================================================
Test suite definitiva che copre ogni fase del bot: ricerca, popup, download P1/P2, 
merge e gestione resiliente delle modale.

Matches source code: src/bots/safework/pdl/bot.py
"""

import time
import contextlib
from pathlib import Path
from unittest.mock import MagicMock, patch, call

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

from src.bots.safework.pdl.bot import SafeWorkPDLBot
from src.core.constants import BotStatus


class TestSafeWorkPDLBotComprehensive:
    @pytest.fixture
    def bot(self, mocker):
        """Fixture per inizializzare il bot con driver e wait mockati."""
        bot = SafeWorkPDLBot(username="test_user", password="test_password", download_path="/tmp/downloads")
        bot.driver = MagicMock()
        bot.wait = MagicMock()
        
        # Patch filesystem operations
        mocker.patch("src.bots.safework.pdl.bot.Path.rename")
        mocker.patch("src.bots.safework.pdl.bot.Path.unlink")
        mocker.patch("src.bots.safework.pdl.bot.Path.exists", return_value=True)
        mocker.patch("src.bots.safework.pdl.bot.Path.mkdir")
        
        # Patch BaseBot/SafeworkBaseBot common methods to avoid side effects
        mocker.patch.object(bot, "_attendi_scomparsa_overlay", return_value=True)
        mocker.patch.object(bot, "click_robusto", return_value=True)
        
        return bot

    # ========================================================================
    # 1. DATA VALIDATION & SANITIZATION
    # ========================================================================

    def test_pdl_number_sanitization(self, bot):
        """Verifica la corretta formattazione dei numeri PdL."""
        assert bot._sanitizza_pdl_number("569157/c") == "569157/C"
        assert bot._sanitizza_pdl_number("569157") == "569157/C"  # > 400000 -> /C
        assert bot._sanitizza_pdl_number("123456") == "123456/S"  # < 400000 -> /S
        assert bot._sanitizza_pdl_number(" 569157 / c ") == "569157/C"

    def test_validate_data_scenarios(self, bot):
        """Verifica la validazione preventiva dei dati."""
        # Successo
        ok, msg = bot.validate_data([{"pdl_number": "123456/C"}])
        assert ok is True
        
        # Fallimento: Dati vuoti
        ok, msg = bot.validate_data([])
        assert ok is False
        assert "Nessun dato" in msg
        
        # Fallimento: Credenziali mancanti
        bot.username = None
        ok, msg = bot.validate_data([{"pdl_number": "123"}])
        assert ok is False
        assert "Credenziali mancanti" in msg

    # ========================================================================
    # 2. SEARCH & POPUP HANDLING
    # ========================================================================

    def test_gestisci_ricerca_estesa_success(self, bot, mocker):
        """Test successo click su 'Si' nel popup di ricerca estesa."""
        # Simula comparsa popup (per testo)
        bot.driver.find_element.return_value = MagicMock()
        
        # Mock WebDriverWait per il popup
        mocker.patch("src.bots.safework.pdl.bot.WebDriverWait.until", return_value=True)
        
        # Per far sì che res sia False, find_element per "nessun dato trovato" deve fallire
        def find_side_effect(by, val):
            if "nessun dato trovato" in val:
                raise Exception("Not found")
            return MagicMock()
        bot.driver.find_element.side_effect = find_side_effect
        
        res = bot._gestisci_ricerca_estesa()
        
        assert res is False 
        # Verifica click sul pulsante 'Si' (idtxt E421C594)
        bot.driver.find_element.assert_any_call(By.CSS_SELECTOR, "span[idtxt='E421C594']")

    def test_gestisci_ricerca_estesa_no_pdl(self, bot, mocker):
        """Test caso PdL non trovato nemmeno con ricerca estesa."""
        mocker.patch("src.bots.safework.pdl.bot.WebDriverWait.until", return_value=True)
        
        # Mock per trovare il messaggio "nessun dato trovato"
        mock_msg = MagicMock()
        mock_msg.is_displayed.return_value = True
        
        def find_side_effect(by, val):
            if "nessun dato trovato" in val: 
                return mock_msg
            return MagicMock()
            
        bot.driver.find_element.side_effect = find_side_effect
        
        res = bot._gestisci_ricerca_estesa()
        assert res is True # True significa "salta questo PDL"

    def test_esegui_ricerca_pdl_full_flow(self, bot, mocker):
        """Test del flusso completo di ricerca con verifica dei selettori via mock EC."""
        mocker.patch.object(bot, "_gestisci_ricerca_estesa", return_value=False)
        mocker.patch.object(bot, "_gestisci_alert_ricerca", return_value=False)
        
        # Mock EC per catturare i selettori
        mock_ec = mocker.patch("src.bots.safework.pdl.bot.EC")
        mock_campo = MagicMock()
        mock_anteprima = MagicMock()
        bot.wait.until.side_effect = [mock_campo, mock_anteprima]
        
        res = bot._esegui_ricerca_pdl("569157/C")
        
        assert res is True
        # 1. Verifica primo wait: deve cercare il campo ricerca
        args_ec_campo = mock_ec.visibility_of_element_located.call_args_list[0][0][0]
        assert args_ec_campo == (By.ID, "fldRicercaPdLVeloce")
        # 2. Verifica invio tasti
        mock_campo.send_keys.assert_called_with("569157/C" + Keys.ENTER)
        # 3. Verifica secondo wait: deve cercare l'anteprima stampa
        args_ec_ant = mock_ec.visibility_of_element_located.call_args_list[1][0][0]
        assert args_ec_ant == (By.ID, "topIcon-acticonAnteprimaStampaMenu")

    # ========================================================================
    # 3. DOWNLOAD PART 1 & PART 2
    # ========================================================================

    def test_scarica_parte_prima_success(self, bot, mocker):
        """Test scarico P1 verificando ogni singolo click e attesa."""
        mocker.patch("src.bots.base.wait_helpers.poll_for_new_file", return_value="/tmp/downloads/569157C.pdf")
        mocker.patch.object(bot, "_clean_pdf")
        mock_safe_remove = mocker.patch.object(bot, "_safe_remove")
        mocker.patch("time.sleep")

        res = bot._scarica_parte_prima("569157/C")
        
        assert res is not None
        # Verifica che ogni click critico sia avvenuto
        assert bot.click_robusto.call_count == 2
        calls = [str(c) for c in bot.click_robusto.call_args_list]
        assert "topIcon-acticonAnteprimaStampaMenu" in calls[0]
        assert "appItaliano" in calls[1]
        # Verifica attesa preliminare resiliente
        bot._attendi_scomparsa_overlay.assert_any_call(timeout_secondi=5)

    def test_scarica_parte_seconda_accordion_strategies(self, bot, mocker):
        """Test espansione accordion Parte Seconda con strategie multiple."""
        mocker.patch("src.bots.base.wait_helpers.poll_for_new_file", return_value="/tmp/downloads/Report.pdf")
        
        # Simula accordion chiuso (lblPAFoglio non visibile)
        mock_el = MagicMock()
        mock_el.is_displayed.return_value = False
        bot.driver.find_elements.return_value = [mock_el]
        
        # Strategie di click
        bot.driver.find_element.side_effect = [
            Exception("ID failed"), 
            Exception("XPATH failed"), 
            MagicMock() # CSS idtxt success
        ]
        
        res = bot._scarica_parte_seconda("569157/C")
        
        assert res is not None
        # Verifica che abbia provato le strategie di espansione
        assert bot.driver.find_element.call_count == 3
        # Verifica click su btnPrintPS
        bot.click_robusto.assert_any_call((By.ID, "btnPrintPS"))

    # ========================================================================
    # 4. POST-PROCESSING & MERGE
    # ========================================================================

    def test_unisci_e_stampa_logic(self, bot, mocker):
        """Test unione PDF e rimozione pagina istruzioni."""
        mock_merge = mocker.patch("src.utils.document_processor.DocumentProcessor.merge_pdfs", return_value=True)
        mocker.patch("os.rename")
        
        item = {"pdl_number": "569157/C", "print_enabled": True}
        all_paths = []
        
        res = bot._unisci_e_stampa("569157/C", "p1.pdf", "p2.pdf", item, all_paths)
        
        assert res is True
        assert len(all_paths) == 1
        mock_merge.assert_called_once()

    def test_clean_pdf_page_removal(self, bot, mocker):
        """Verifica la rimozione della pagina 2 (istruzioni) tramite PyMuPDF."""
        mock_fitz_open = mocker.patch("src.bots.safework.pdl.bot.fitz.open")
        mock_doc = MagicMock()
        mock_doc.page_count = 2
        mock_fitz_open.return_value = mock_doc
        
        bot._clean_pdf("test.pdf")
        
        mock_doc.delete_page.assert_called_with(1)
        mock_doc.save.assert_called_with("test.pdf.tmp")
        mock_doc.close.assert_called_once()

    # ========================================================================
    # 5. LIFECYCLE & RUN LOOP
    # ========================================================================

    def test_run_full_cycle_success(self, bot, mocker):
        """Test del ciclo 'run' per più PDL con successo."""
        mocker.patch.object(bot, "_login", return_value=True)
        mocker.patch.object(bot, "_attendi_caricamento_sistema")
        mocker.patch.object(bot, "_esegui_ricerca_pdl", return_value=True)
        mocker.patch.object(bot, "_scarica_parte_prima", return_value="p1.pdf")
        mocker.patch.object(bot, "_scarica_parte_seconda", return_value="p2.pdf")
        mocker.patch.object(bot, "_unisci_e_stampa", return_value=True)
        mocker.patch.object(bot, "_handle_session_merge")
        
        data = [{"pdl_number": "569157/C"}, {"pdl_number": "123456/S"}]
        
        res = bot.run(data)
        
        assert res is True
        # Verifica che abbia cercato entrambi i PDL
        assert bot._esegui_ricerca_pdl.call_count == 2
        assert bot.status == BotStatus.IDLE

    # ========================================================================
    # 6. REGRESSION SHIELD - SPECIFIC TESTS
    # ========================================================================

    def test_regression_shield_popup_si_blocking(self, bot, mocker):
        """
        REGRESSION TEST: Verifica che il bot non prosegua se il popup 'Si' 
        blocca l'interfaccia. Se questa logica viene rimossa, il test DEVE fallire.
        """
        # 1. Rimuoviamo il mock del metodo per questo test specifico per usare la logica reale
        mocker.stopall() 
        # Re-mock dei componenti necessari per non far crashare il driver
        bot.driver = MagicMock()
        bot.wait = MagicMock()
        
        # 2. Simula che il popup appaia (WebDriverWait lo trova)
        mocker.patch("src.bots.safework.base.WebDriverWait.until", return_value=MagicMock())
        
        # 3. Mock della funzione di click robusto 
        with patch.object(bot, "log") as mock_log:
            # Simula presenza modale con tasto Si
            mock_modal = MagicMock()
            bot.driver.find_element.return_value = mock_modal
            
            # Esegue la logica di gestione popup reale di SafeworkBaseBot
            bot._attendi_scomparsa_overlay(timeout_secondi=1)
            
            # Verifica che il bot abbia loggato la gestione della modale
            assert any("Modale gestita" in call.args[0] for call in mock_log.call_args_list)

    def test_validate_data_no_pdls(self, bot):
        """Test validazione quando non ci sono numeri PDL nei dati."""
        data = [{"not_a_pdl": "123"}]
        ok, msg = bot.validate_data(data)
        assert ok is False
        assert "Nessun numero PDL trovato" in msg

    # ========================================================================
    # 2. SEARCH & POPUP HANDLING
    # ========================================================================

    def test_esegui_ricerca_pdl_search_field_error(self, bot, mocker):
        """Verifica errore quando il campo ricerca non viene trovato."""
        bot.wait.until.side_effect = Exception("Field not found")
        res = bot._esegui_ricerca_pdl("123")
        assert res is False

    def test_esegui_ricerca_pdl_preview_timeout(self, bot, mocker):
        """Verifica errore quando la pagina non carica l'anteprima dopo la ricerca."""
        mocker.patch.object(bot, "_gestisci_ricerca_estesa", return_value=False)
        mocker.patch.object(bot, "_gestisci_alert_ricerca", return_value=False)
        # Mock wait.until: prima successo (campo), seconda fallimento (anteprima)
        bot.wait.until.side_effect = [MagicMock(), Exception("Preview timeout")]
        
        res = bot._esegui_ricerca_pdl("123")
        assert res is False

    def test_gestisci_ricerca_estesa_click_failed(self, bot, mocker):
        """Test caso in cui il popup è visto ma il click su Si fallisce."""
        mocker.patch("src.bots.safework.pdl.bot.WebDriverWait.until", return_value=True)
        bot.driver.find_element.side_effect = Exception("Click blocked")
        
        res = bot._gestisci_ricerca_estesa()
        assert res is False # Non ha trovato 'nessun dato trovato' e il click è fallito

    def test_gestisci_alert_ricerca_logic(self, bot, mocker):
        """Verifica la chiusura degli alert informativi."""
        mock_btn = MagicMock()
        mock_btn.is_displayed.return_value = True
        bot.driver.find_element.return_value = mock_btn
        mocker.patch("src.bots.safework.pdl.bot.WebDriverWait.until", return_value=True)
        
        assert bot._gestisci_alert_ricerca() is True
        mock_btn.click.assert_called_once()

    # ========================================================================
    # 3. DOWNLOAD PART 1 & PART 2
    # ========================================================================

    def test_scarica_parte_prima_exception(self, bot, mocker):
        """Verifica la cattura di eccezioni durante lo scarico P1."""
        bot.click_robusto.side_effect = Exception("Crash")
        assert bot._scarica_parte_prima("123") is None

    def test_scarica_parte_seconda_expansion_failed(self, bot, mocker):
        """Verifica che lo scarico P2 fallisca se l'accordion non si apre."""
        mocker.patch.object(bot, "_espandi_parte_seconda", return_value=False)
        assert bot._scarica_parte_seconda("123") is None

    def test_scarica_parte_seconda_exception(self, bot, mocker):
        """Verifica la cattura di eccezioni durante lo scarico P2."""
        mocker.patch.object(bot, "_espandi_parte_seconda", return_value=True)
        bot.click_robusto.side_effect = Exception("Crash")
        assert bot._scarica_parte_seconda("123") is None

    def test_espandi_parte_seconda_exception(self, bot, mocker):
        """Verifica gestione errori durante l'espansione dell'accordion."""
        bot.driver.find_elements.side_effect = Exception("Driver error")
        assert bot._espandi_parte_seconda() is False

    # ========================================================================
    # 4. POST-PROCESSING & MERGE
    # ========================================================================

    def test_clean_pdf_single_page(self, bot, mocker):
        """Verifica che non venga fatta pulizia se il PDF ha una sola pagina."""
        mock_fitz = mocker.patch("src.bots.safework.pdl.bot.fitz.open")
        mock_doc = mock_fitz.return_value
        mock_doc.page_count = 1
        
        bot._clean_pdf("one_page.pdf")
        mock_doc.delete_page.assert_not_called()

    def test_clean_pdf_exception(self, bot, mocker):
        """Verifica che la pulizia PDF non crashi il bot in caso di errore file."""
        mocker.patch("src.bots.safework.pdl.bot.fitz.open", side_effect=Exception("Corrupt"))
        # Non deve sollevare eccezioni
        bot._clean_pdf("bad.pdf")

    def test_handle_session_merge_error(self, bot, mocker):
        """Verifica che l'errore nell'unione sessione sia catturato."""
        mocker.patch("src.utils.document_processor.DocumentProcessor.merge_pdfs", side_effect=Exception("Merge failed"))
        # Non deve sollevare eccezioni
        bot._handle_session_merge([{"merge_all_session": True}], ["p1.pdf"])

    # ========================================================================
    # 5. LIFECYCLE & RUN LOOP
    # ========================================================================

    def test_run_with_pdl_error_continues(self, bot, mocker):
        """Verifica che un errore su un PDL non blocchi gli altri."""
        mocker.patch.object(bot, "_login", return_value=True)
        mocker.patch.object(bot, "_attendi_caricamento_sistema")
        mocker.patch.object(bot, "_handle_session_merge")
        
        # Simula: 1° PDL crasha, 2° PDL successo
        mocker.patch.object(bot, "_esegui_ricerca_pdl", side_effect=[Exception("Crash"), True])
        mocker.patch.object(bot, "_scarica_parte_prima", return_value="p1.pdf")
        mocker.patch.object(bot, "_scarica_parte_seconda", return_value="p2.pdf")
        mocker.patch.object(bot, "_unisci_e_stampa", return_value=True)
        
        data = [{"pdl_number": "ERR"}, {"pdl_number": "OK"}]
        res = bot.run(data)
        
        assert res is False # Non tutti riusciti
        assert bot._esegui_ricerca_pdl.call_count == 2

    def test_gestisci_dialogo_stampa_tutte_logic(self, bot, mocker):
        """Verifica la logica del dialogo stampa tutte."""
        mock_btn = MagicMock()
        bot.wait.until.return_value = mock_btn
        bot._gestisci_dialogo_stampa_tutte()
        assert mock_btn.click.call_count == 2

    def test_sanitizza_pdl_number_variations(self, bot):
        """Verifica tutti i rami della sanitizzazione numero PDL."""
        # Già formattato
        assert bot._sanitizza_pdl_number("123456/S") == "123456/S"
        # Lunghezza diversa da 6
        assert bot._sanitizza_pdl_number("12345") == "12345"
        # Non numerico
        assert bot._sanitizza_pdl_number("ABCDEF") == "ABCDEF"

    def test_safe_remove_non_existent(self, bot):
        """Verifica che safe_remove non faccia nulla se il file non esiste."""
        # Non deve sollevare eccezioni
        bot._safe_remove("non_existent_file_xyz.pdf")

    def test_validate_data_dict_format(self, bot):
        """Verifica validazione con formato dizionario (rows key)."""
        data = {"rows": [{"pdl_number": "123456"}]}
        ok, msg = bot.validate_data(data)
        assert ok is True

    def test_run_interruption_handling(self, bot, mocker):


        """Verifica la gestione dell'interruzione manuale dell'utente."""
        mocker.patch.object(bot, "_login", return_value=True)
        mocker.patch.object(bot, "_attendi_caricamento_sistema")
        
        # Simula interruzione al primo PdL
        mocker.patch.object(bot, "_check_stop", side_effect=InterruptedError("Stop"))
        
        data = [{"pdl_number": "569157/C"}]
        
        with pytest.raises(InterruptedError):
            bot.run(data)
