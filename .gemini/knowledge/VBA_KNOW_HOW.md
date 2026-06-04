# Knowledge Base VBA: master_consuntivo_Automatico.xlsm

Questo file contiene il codice estratto senza l'uso di Excel (bypassando gli errori UI).

## Componente: Questa_cartella_di_lavoro.cls
Stream: VBA/Questa_cartella_di_lavoro

```vba
Attribute VB_Name = "Questa_cartella_di_lavoro"
Attribute VB_Base = "0{00020819-0000-0000-C000-000000000046}"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Attribute VB_TemplateDerived = False
Attribute VB_Customizable = True

```

## Componente: Foglio5.cls
Stream: VBA/Foglio5

```vba
Attribute VB_Name = "Foglio5"
Attribute VB_Base = "0{00020820-0000-0000-C000-000000000046}"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Attribute VB_TemplateDerived = False
Attribute VB_Customizable = True

```

## Componente: Foglio6.cls
Stream: VBA/Foglio6

```vba
Attribute VB_Name = "Foglio6"
Attribute VB_Base = "0{00020820-0000-0000-C000-000000000046}"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Attribute VB_TemplateDerived = False
Attribute VB_Customizable = True

```

## Componente: Foglio3.cls
Stream: VBA/Foglio3

```vba
Attribute VB_Name = "Foglio3"
Attribute VB_Base = "0{00020820-0000-0000-C000-000000000046}"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Attribute VB_TemplateDerived = False
Attribute VB_Customizable = True

```

## Componente: Foglio4.cls
Stream: VBA/Foglio4

```vba
Attribute VB_Name = "Foglio4"
Attribute VB_Base = "0{00020820-0000-0000-C000-000000000046}"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Attribute VB_TemplateDerived = False
Attribute VB_Customizable = True

```

## Componente: Foglio1.cls
Stream: VBA/Foglio1

```vba
Attribute VB_Name = "Foglio1"
Attribute VB_Base = "0{00020820-0000-0000-C000-000000000046}"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Attribute VB_TemplateDerived = False
Attribute VB_Customizable = True

```

## Componente: Modulo1.bas
Stream: VBA/Modulo1

```vba
Attribute VB_Name = "Modulo1"
Option Explicit

'da modificare anche modulo 41 nel caso in cui si modifica il codice di verifica consuntivo
Sub verificaEstampaFogli()

    Dim msgError As String
    Dim wsConsuntivo As Worksheet, wsRifVBA As Worksheet
    ' Dim i As Long ' Variabile i non è usata

    ' Variabili per ripristino impostazioni Applicazione
    Dim prevStatusBar As Variant
    Dim prevEnableEvents As Boolean
    Dim prevScreenUpdating As Boolean
    Dim prevCalculation As XlCalculation
    Dim erroreVBAPresente As Boolean ' Flag per sapere se si è verificato un errore VBA

    erroreVBAPresente = False

    ' Salva lo stato corrente delle impostazioni e le modifica
    prevStatusBar = Application.StatusBar
    prevEnableEvents = Application.EnableEvents
    prevScreenUpdating = Application.ScreenUpdating
    prevCalculation = Application.Calculation

    Application.EnableEvents = False
    Application.ScreenUpdating = False
    Application.Calculation = xlCalculationManual
    Application.StatusBar = "Verifica dati per stampa in corso..."

    On Error GoTo GestoreErroriImprevisti

    Set wsConsuntivo = ThisWorkbook.Sheets("Consuntivo")
    Set wsRifVBA = ThisWorkbook.Sheets("rif.VBA")

    ' Verifica cella C4 nel foglio rif.VBA
    If wsRifVBA.Range("C4").Value = "" Then msgError = msgError & "Inserire assistente TCL." & vbCrLf

    ' Verifica celle vuote nel foglio Consuntivo
    If Trim(wsConsuntivo.Range("A22").Value) = "" Then msgError = msgError & "Il consuntivo risulta vuoto." & vbCrLf
    If wsConsuntivo.Range("J10").Value = "" Then msgError = msgError & "Inserisci data." & vbCrLf
    If wsConsuntivo.Range("D14").Value = "" Then msgError = msgError & "Inserisci descrizione lavoro." & vbCrLf
    If wsConsuntivo.Range("J14").Value = "" Or InStr(1, CStr(wsConsuntivo.Range("J14").Value), "ERRORE", vbTextCompare) > 0 Then msgError = msgError & "Mancato rilevamento formato nome file o errore rilevato." & vbCrLf
    If wsConsuntivo.Range("B56").Value = "" Or wsConsuntivo.Range("K16").Value = "" Then msgError = msgError & "Inserisci Persona che compila il consuntivo o controlla la cella K16." & vbCrLf
    If wsConsuntivo.Range("H12").Value = "" Or wsConsuntivo.Range("H56").Value = "" Then msgError = msgError & "Inserisci Assistente TCL o controlla la cella H56." & vbCrLf

    ' Verifica uguaglianza ore spese, solo se B4 di rif.VBA è diverso da "MISURA"
    If UCase(Trim(CStr(wsRifVBA.Range("B4").Value))) <> "MISURA" Then
        On Error Resume Next
        Dim valP21 As Variant, valQ5 As Variant
        valP21 = wsConsuntivo.Range("P21").Value
        valQ5 = wsConsuntivo.Range("Q5").Value
        If IsNumeric(valP21) And IsNumeric(valQ5) Then
            If CDbl(valP21) <> CDbl(valQ5) Then
                msgError = msgError & "Quantità ore spese attività diversa tra Giornaliera e dettaglio ore (P21 vs Q5)." & vbCrLf
            End If
        Else
            If Not (IsError(valP21) Or IsError(valQ5)) Then
                 msgError = msgError & "Impossibile confrontare ore spese (P21 vs Q5) a causa di valori non numerici o vuoti." & vbCrLf
            End If
        End If
        Err.Clear
        On Error GoTo GestoreErroriImprevisti
    End If

    ' Verifica congruenza economica
    On Error Resume Next
    Dim valJ8 As Variant, valI45 As Variant
    valJ8 = wsConsuntivo.Range("J8").Value
    valI45 = wsConsuntivo.Range("I45").Value
    If IsNumeric(valJ8) And IsNumeric(valI45) Then
        If CDbl(valJ8) <> CDbl(valI45) Then
            msgError = msgError & "La somma economica nel Consuntivo non è congruente (J8 vs I45)." & vbCrLf
        End If
    Else
        If Not (IsError(valJ8) Or IsError(valI45)) Then
            msgError = msgError & "Impossibile confrontare somme economiche (J8 vs I45) a causa di valori non numerici o vuoti." & vbCrLf
        End If
    End If
    Err.Clear
    On Error GoTo GestoreErroriImprevisti

    'Gestione errori #RIF! o altri errori di cella
    If IsError(wsConsuntivo.Range("J10").Value) Then msgError = msgError & "La cella J10 (Data) contiene un errore." & vbCrLf
    If IsError(wsConsuntivo.Range("D14").Value) Then msgError = msgError & "La cella D14 (Descrizione Lavoro) contiene un errore." & vbCrLf
    If IsError(wsConsuntivo.Range("I45").Value) Then msgError = msgError & "La cella I45 (Totale Economico Dettaglio) contiene un errore." & vbCrLf
    If IsError(wsConsuntivo.Range("J14").Value) Then msgError = msgError & "La cella J14 (Nome File) contiene un errore." & vbCrLf
    If IsError(wsConsuntivo.Range("H12").Value) Then msgError = msgError & "La cella H12 (Assistente TCL Riepilogo) contiene un errore." & vbCrLf
    If IsError(wsConsuntivo.Range("P21").Value) Then msgError = msgError & "La cella P21 (Ore Spese Giornaliera) contiene un errore." & vbCrLf
    If IsError(wsConsuntivo.Range("Q5").Value) Then msgError = msgError & "La cella Q5 (Ore Spese Dettaglio) contiene un errore." & vbCrLf
    If IsError(wsConsuntivo.Range("J8").Value) Then msgError = msgError & "La cella J8 (Totale Economico Riepilogo) contiene un errore." & vbCrLf
    If IsError(wsConsuntivo.Range("K16").Value) Then msgError = msgError & "La cella K16 contiene un errore." & vbCrLf
    If IsError(wsConsuntivo.Range("H56").Value) Then msgError = msgError & "La cella H56 contiene un errore." & vbCrLf

    ' Messaggio finale e chiamata a StampaFogli
    If msgError = "" Then
        Application.StatusBar = "Verifica dati completata. Nessun problema rilevato. Avvio stampa..."
        Call StampaFogli ' Chiama la Sub di stampa solo se non ci sono errori
    Else
        Application.StatusBar = "Verifica dati completata. Rilevati problemi! Stampa annullata."
        MsgBox msgError, vbExclamation, "Problemi Rilevati - Stampa Annullata"
    End If

    GoTo RipristinaImpostazioni

GestoreErroriImprevisti:
    erroreVBAPresente = True
    Application.StatusBar = "verificaEstampaFogli: Errore VBA n. " & Err.Number & " - " & Err.Description
    MsgBox "Si è verificato un errore imprevisto nella macro verificaEstampaFogli." & vbCrLf & _
           "Errore " & Err.Number & ": " & Err.Description, vbCritical, "Errore Macro"

RipristinaImpostazioni:
    Application.EnableEvents = prevEnableEvents
    Application.ScreenUpdating = prevScreenUpdating
    Application.Calculation = prevCalculation
    If Not erroreVBAPresente Then
        ' Se non c'è stato un errore VBA, ma msgError potrebbe aver causato un MsgBox di validazione,
        ' la barra di stato potrebbe già avere un messaggio pertinente.
        ' Si resetta solo se non ci sono stati errori VBA e il messaggio di stato non è un errore.
        If InStr(1, Application.StatusBar, "Errore", vbTextCompare) = 0 Then
             Application.StatusBar = False ' Pulisce se non è un messaggio di errore
        End If
    End If ' Se c'è stato un errore VBA, la barra di stato mostra il messaggio di errore VBA
    Set wsConsuntivo = Nothing
    Set wsRifVBA = Nothing
End Sub


Sub StampaFogli()

    Dim wsConsuntivo As Worksheet
    Dim wsTabella As Worksheet
    Dim printAreaConsuntivo As String: printAreaConsuntivo = "A1:L63"
    Dim printAreaStandard As String: printAreaStandard = "A1:AB30"
    Dim sheetNames As Collection
    Dim sheetNameAsVariant As Variant ' Rinominato per evitare conflitto con tipo stringa
    Dim cell As Range
    Dim tipologiaPreventivo As String
    Dim tempSheet As Worksheet ' Per gestire i fogli da stampare
    Dim nomeFoglioDaStampare As String ' Per la barra di stato

    ' Costante per i margini (in punti, 0.2 pollici circa)
    Const MARGINE_MINIMO_POINTS As Double = 14.4 ' Application.InchesToPoints(0.2)

    ' Variabili per ripristino impostazioni Applicazione
    Dim prevStatusBar As Variant
    Dim prevEnableEvents As Boolean
    Dim prevScreenUpdating As Boolean
    Dim erroreVBAPresente As Boolean ' Flag per sapere se si è verificato un errore VBA

    erroreVBAPresente = False

    ' Salva lo stato corrente delle impostazioni e le modifica
    prevStatusBar = Application.StatusBar
    prevEnableEvents = Application.EnableEvents
    prevScreenUpdating = Application.ScreenUpdating

    Application.EnableEvents = False
    Application.ScreenUpdating = False
    ' Calculation non è strettamente necessario qui, ma per coerenza se ci fossero formule in PageSetup
    ' Application.Calculation = xlCalculationManual
    Application.StatusBar = "StampaFogli: Avvio procedura di stampa..."

    On Error GoTo ErrHandlerStampa ' Gestione errori centralizzata per questa Sub

    Set wsConsuntivo = ThisWorkbook.Sheets("Consuntivo")
    Set wsTabella = ThisWorkbook.Sheets("rif.VBA")
    Set sheetNames = New Collection

    ' Controllo della tipologia del preventivo
    tipologiaPreventivo = Trim(CStr(wsTabella.Range("B4").Value)) ' Aggiunto CStr per sicurezza

    If tipologiaPreventivo = "" Then
        MsgBox "Tipologia preventivo non compilata in 'rif.VBA'! Impossibile procedere con la stampa.", vbCritical, "Errore Stampa"
        Application.StatusBar = "StampaFogli: Tipologia preventivo mancante. Stampa annullata."
        GoTo RipristinaImpostazioniStampa
    End If

    ' Stampa il foglio Consuntivo
    nomeFoglioDaStampare = wsConsuntivo.Name
    Application.StatusBar = "StampaFogli: Preparazione stampa foglio '" & nomeFoglioDaStampare & "'..."
    With wsConsuntivo.PageSetup
        .PrintArea = printAreaConsuntivo
        .LeftMargin = MARGINE_MINIMO_POINTS
        .RightMargin = MARGINE_MINIMO_POINTS
        .TopMargin = MARGINE_MINIMO_POINTS
        .BottomMargin = MARGINE_MINIMO_POINTS
        .HeaderMargin = MARGINE_MINIMO_POINTS / 2 ' Margini intestazione/piè di pagina più piccoli
        .FooterMargin = MARGINE_MINIMO_POINTS / 2
        .CenterHorizontally = True ' Opzionale: centra orizzontalmente
        .Zoom = False ' Assicura che non ci sia uno zoom preimpostato che interferisca
        .FitToPagesWide = 1 ' Adatta a una pagina in larghezza
        .FitToPagesTall = False ' Permette di usare più pagine in altezza se necessario (non comprime verticalmente)
    End With
    wsConsuntivo.PrintOut Copies:=1, Collate:=True ' Parametri di stampa standard

    ' Se la tipologia è diversa da "MISURA", raccogli e stampa i nomi degli altri fogli
    If UCase(tipologiaPreventivo) <> "MISURA" Then
        ' Raccogli i nomi dei fogli da Tabella10
        If wsTabella.ListObjects.Count > 0 Then ' Controlla se ci sono tabelle
            On Error Resume Next ' Se Tabella10 non esiste
            Dim lo As ListObject
            Set lo = wsTabella.ListObjects("Tabella10")
            On Error GoTo ErrHandlerStampa ' Ripristina gestore principale

            If Not lo Is Nothing Then
                If lo.ListColumns.Count > 0 Then
                    If Not lo.DataBodyRange Is Nothing Then ' Controlla se ci sono dati nella tabella
                        For Each cell In lo.ListColumns(1).DataBodyRange.Cells ' Usa .Cells per iterare correttamente
                            If Trim(CStr(cell.Value)) <> "" Then ' Aggiunge solo nomi non vuoti
                                sheetNames.Add Trim(CStr(cell.Value))
                            End If
                        Next cell
                    End If
                Else
                    Application.StatusBar = "StampaFogli: Tabella10 non ha colonne."
                End If
            Else
                Application.StatusBar = "StampaFogli: Tabella10 non trovata in 'rif.VBA'."
            End If
        Else
            Application.StatusBar = "StampaFogli: Nessuna tabella trovata in 'rif.VBA'."
        End If


        ' Stampa i fogli raccolti
        If sheetNames.Count > 0 Then
            Application.StatusBar = "StampaFogli: Inizio stampa di " & sheetNames.Count & " fogli aggiuntivi..."
            For Each sheetNameAsVariant In sheetNames
                nomeFoglioDaStampare = CStr(sheetNameAsVariant)

                On Error Resume Next ' Per gestire nomi foglio non validi
                Set tempSheet = Nothing
                Set tempSheet = ThisWorkbook.Sheets(nomeFoglioDaStampare)
                On Error GoTo ErrHandlerStampa ' Ripristina gestore principale

                If Not tempSheet Is Nothing Then
                    Application.StatusBar = "StampaFogli: Preparazione stampa foglio '" & nomeFoglioDaStampare & "'..."
                    With tempSheet.PageSetup
                        .PrintArea = printAreaStandard
                        .LeftMargin = MARGINE_MINIMO_POINTS
                        .RightMargin = MARGINE_MINIMO_POINTS
                        .TopMargin = MARGINE_MINIMO_POINTS
                        .BottomMargin = MARGINE_MINIMO_POINTS
                        .HeaderMargin = MARGINE_MINIMO_POINTS / 2
                        .FooterMargin = MARGINE_MINIMO_POINTS / 2
                        .CenterHorizontally = True
                        .Zoom = False
                        .FitToPagesWide = 1
                        .FitToPagesTall = False
                    End With
                    tempSheet.PrintOut Copies:=1, Collate:=True
                Else
                    Application.StatusBar = "StampaFogli: Foglio '" & nomeFoglioDaStampare & "' non trovato o non valido. Saltato."
                    ' Potresti voler loggare questo errore o informare l'utente in modo non bloccante se necessario
                End If
            Next sheetNameAsVariant
        Else
             Application.StatusBar = "StampaFogli: Nessun foglio aggiuntivo valido da stampare per tipologia '" & tipologiaPreventivo & "'."
        End If
    End If

    Application.StatusBar = "StampaFogli: Procedura di stampa completata."
    Application.Wait Now + TimeValue("00:00:02") ' Pausa per visualizzare il messaggio

RipristinaImpostazioniStampa:
    Application.EnableEvents = prevEnableEvents
    Application.ScreenUpdating = prevScreenUpdating
    ' Application.Calculation = prevCalculation ' Se abilitato all'inizio
    If Not erroreVBAPresente Then
        Application.StatusBar = False
    End If ' Se erroreVBAPresente, la barra di stato mostra l'errore VBA
    Set wsConsuntivo = Nothing
    Set wsTabella = Nothing
    Set sheetNames = Nothing
    Set tempSheet = Nothing
    Set lo = Nothing
    Exit Sub

ErrHandlerStampa:
    erroreVBAPresente = True
    Application.StatusBar = "StampaFogli: Errore VBA n. " & Err.Number & " - " & Err.Description
    MsgBox "Errore " & Err.Number & " durante la stampa: " & Err.Description, vbCritical, "Errore Stampa"
    Resume RipristinaImpostazioniStampa
End Sub




```

## Componente: Foglio7.cls
Stream: VBA/Foglio7

```vba
Attribute VB_Name = "Foglio7"
Attribute VB_Base = "0{00020820-0000-0000-C000-000000000046}"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Attribute VB_TemplateDerived = False
Attribute VB_Customizable = True

```

## Componente: Modulo18.bas
Stream: VBA/Modulo18

```vba
Attribute VB_Name = "Modulo18"
Sub SmistaDatiGiorno10()
    Dim wsOrigine As Worksheet, wsDestinazione As Worksheet
    Dim ultimaRiga As Long, i As Long
    Dim data As Date, dataGiorno10 As Date
    Dim rigaDestinazione As Long
    Dim concatenatoA24 As String
    Dim concatenatoU24 As String
    Dim valoreC As String
    Dim valoreD As String
    Dim valoriC As Collection
    Dim valoriD As Collection
    Dim almenoUnaCorrispondenza As Boolean

    ' Imposta i fogli
    Set wsOrigine = ThisWorkbook.Sheets("Elabora Giornaliera")
    Set wsDestinazione = ThisWorkbook.Sheets("10")

    ' Trova l'ultima riga con dati nel foglio di origine
    ultimaRiga = wsOrigine.Cells(Rows.Count, 1).End(xlUp).Row

    ' Inizializza la riga di partenza per le colonne
    rigaDestinazione = 11

    ' Inizializza le celle di destinazione A24 e U24
    concatenatoA24 = ""
    concatenatoU24 = ""

    ' Inizializza le collezioni per rimuovere duplicati
    Set valoriC = New Collection
    Set valoriD = New Collection

    almenoUnaCorrispondenza = False

    'Gestisci potenziale errore in K11
    On Error Resume Next
    dataGiorno10 = DateValue(Worksheets("Elabora Giornaliera").Range("K11").Value)
    On Error GoTo 0

    'Controlla se la conversione della data è fallita
    If IsDate(dataGiorno10) Then
        ' Ciclo attraverso le righe del foglio di origine
        For i = 1 To ultimaRiga
            ' Controlla se la riga è vuota
            If IsEmpty(wsOrigine.Cells(i, 1).Value) Then Exit For

            On Error Resume Next
            data = CDate(Trim(wsOrigine.Cells(i, 1).Value))
            On Error GoTo 0

            ' Controlla se la data è uguale a dataGiorno10
            If data = dataGiorno10 Then
                almenoUnaCorrispondenza = True
                ' Verifica se riga destinazione non è 21 o 23
                If rigaDestinazione <> 21 And rigaDestinazione <> 23 Then
                    ' Copia i valori
                    wsDestinazione.Cells(rigaDestinazione, 1).Value = wsOrigine.Cells(i, 2).Value
                    wsDestinazione.Cells(rigaDestinazione, 4).Value = wsOrigine.Cells(i, 5).Value
                    wsDestinazione.Cells(rigaDestinazione, 5).Value = wsOrigine.Cells(i, 6).Value
                End If

                ' Aggiungi valori a A24 e U24, gestendo errori di conversione
                valoreC = Trim(wsOrigine.Cells(i, 3).Value)
                If Not IsEmpty(valoreC) Then
                    If Not ValoreEsistente(valoriC, valoreC) Then
                        valoriC.Add valoreC
                        concatenatoA24 = concatenatoA24 & IIf(concatenatoA24 = "", "", vbCrLf) & valoreC
                    End If
                End If

                valoreD = Trim(wsOrigine.Cells(i, 4).Value)
                If Not IsEmpty(valoreD) Then
                    If Not ValoreEsistente(valoriD, valoreD) Then
                        valoriD.Add valoreD
                        concatenatoU24 = concatenatoU24 & IIf(concatenatoU24 = "", "", vbCrLf) & valoreD
                    End If
                End If

                rigaDestinazione = rigaDestinazione + 1
            End If
        Next i

        ' Assegna le concatenazioni alle celle A24 e U24
        wsDestinazione.Range("A24").Value = concatenatoA24
        wsDestinazione.Range("U24").Value = concatenatoU24
    Else
        MsgBox "La cella K11 del foglio 'Elabora Giornaliera' non contiene una data valida.", vbExclamation
    End If

    Application.CutCopyMode = False
    Set valoriC = Nothing
    Set valoriD = Nothing
    Set wsOrigine = Nothing
    Set wsDestinazione = Nothing

End Sub

Function ValoreEsistente(valori As Collection, valore As String) As Boolean
    Dim v As Variant
    On Error Resume Next
    For Each v In valori
        If v = valore Then
            ValoreEsistente = True
            Exit Function
        End If
    Next v
    ValoreEsistente = False
End Function


```

## Componente: Modulo9.bas
Stream: VBA/Modulo9

```vba
Attribute VB_Name = "Modulo9"
Sub SmistaDatiGiorno2()
    Dim wsOrigine As Worksheet, wsDestinazione As Worksheet
    Dim ultimaRiga As Long, i As Long
    Dim data As Date, dataGiorno2 As Date
    Dim rigaDestinazione As Long
    Dim concatenatoA24 As String
    Dim concatenatoU24 As String
    Dim valoreC As String
    Dim valoreD As String
    Dim valoriC As Collection
    Dim valoriD As Collection
    Dim almenoUnaCorrispondenza As Boolean

    ' Imposta i fogli
    Set wsOrigine = ThisWorkbook.Sheets("Elabora Giornaliera")
    Set wsDestinazione = ThisWorkbook.Sheets("2")

    ' Trova l'ultima riga con dati nel foglio di origine
    ultimaRiga = wsOrigine.Cells(Rows.Count, 1).End(xlUp).Row

    ' Inizializza la riga di partenza per le colonne
    rigaDestinazione = 11

    ' Inizializza le celle di destinazione A24 e U24
    concatenatoA24 = ""
    concatenatoU24 = ""

    ' Inizializza le collezioni per rimuovere duplicati
    Set valoriC = New Collection
    Set valoriD = New Collection

    almenoUnaCorrispondenza = False

    'Gestisci potenziale errore in K3
    On Error Resume Next
    dataGiorno2 = DateValue(Worksheets("Elabora Giornaliera").Range("K3").Value)
    On Error GoTo 0

    'Controlla se la conversione della data è fallita (dataGiorno2 è una data valida)
    If IsDate(dataGiorno2) Then
        ' Ciclo attraverso le righe del foglio di origine
        For i = 1 To ultimaRiga
            ' Controlla se la riga è vuota (verifica su colonna A)
            If IsEmpty(wsOrigine.Cells(i, 1).Value) Then Exit For ' Esce solo dal ciclo For

            On Error Resume Next
            data = CDate(Trim(wsOrigine.Cells(i, 1).Value))
            On Error GoTo 0

            ' Controlla se la data è uguale a dataGiorno2
            If data = dataGiorno2 Then
                almenoUnaCorrispondenza = True
                ' Verifica se riga destinazione non è 21 o 23
                If rigaDestinazione <> 21 And rigaDestinazione <> 23 Then
                    ' Copia i valori
                    wsDestinazione.Cells(rigaDestinazione, 1).Value = wsOrigine.Cells(i, 2).Value
                    wsDestinazione.Cells(rigaDestinazione, 4).Value = wsOrigine.Cells(i, 5).Value
                    wsDestinazione.Cells(rigaDestinazione, 5).Value = wsOrigine.Cells(i, 6).Value
                End If

                ' Aggiungi valori a A24 e U24, gestendo errori di conversione
                valoreC = Trim(wsOrigine.Cells(i, 3).Value)
                If Not IsEmpty(valoreC) Then
                    If Not ValoreEsistente(valoriC, valoreC) Then
                        valoriC.Add valoreC
                        concatenatoA24 = concatenatoA24 & IIf(concatenatoA24 = "", "", vbCrLf) & valoreC
                    End If
                End If

                valoreD = Trim(wsOrigine.Cells(i, 4).Value)
                If Not IsEmpty(valoreD) Then
                    If Not ValoreEsistente(valoriD, valoreD) Then
                        valoriD.Add valoreD
                        concatenatoU24 = concatenatoU24 & IIf(concatenatoU24 = "", "", vbCrLf) & valoreD
                    End If
                End If

                rigaDestinazione = rigaDestinazione + 1
            End If
        Next i

        ' Assegna le concatenazioni alle celle A24 e U24
        wsDestinazione.Range("A24").Value = concatenatoA24
        wsDestinazione.Range("U24").Value = concatenatoU24
    Else
        MsgBox "La cella K3 del foglio 'Elabora Giornaliera' non contiene una data valida.", vbExclamation 'Messaggio se K3 non è una data valida.
    End If

    Application.CutCopyMode = False
    Set valoriC = Nothing
    Set valoriD = Nothing
    Set wsOrigine = Nothing
    Set wsDestinazione = Nothing

End Sub

Function ValoreEsistente(valori As Collection, valore As String) As Boolean
    Dim v As Variant
    On Error Resume Next
    For Each v In valori
        If v = valore Then
            ValoreEsistente = True
            Exit Function
        End If
    Next v
    ValoreEsistente = False
End Function


```

## Componente: Modulo17.bas
Stream: VBA/Modulo17

```vba
Attribute VB_Name = "Modulo17"
Sub SmistaDatiGiorno9()
    Dim wsOrigine As Worksheet, wsDestinazione As Worksheet
    Dim ultimaRiga As Long, i As Long
    Dim data As Date, dataGiorno9 As Date
    Dim rigaDestinazione As Long
    Dim concatenatoA24 As String
    Dim concatenatoU24 As String
    Dim valoreC As String
    Dim valoreD As String
    Dim valoriC As Collection
    Dim valoriD As Collection
    Dim almenoUnaCorrispondenza As Boolean

    ' Imposta i fogli
    Set wsOrigine = ThisWorkbook.Sheets("Elabora Giornaliera")
    Set wsDestinazione = ThisWorkbook.Sheets("9")

    ' Trova l'ultima riga con dati nel foglio di origine
    ultimaRiga = wsOrigine.Cells(Rows.Count, 1).End(xlUp).Row

    ' Inizializza la riga di partenza per le colonne
    rigaDestinazione = 11

    ' Inizializza le celle di destinazione A24 e U24
    concatenatoA24 = ""
    concatenatoU24 = ""

    ' Inizializza le collezioni per rimuovere duplicati
    Set valoriC = New Collection
    Set valoriD = New Collection

    almenoUnaCorrispondenza = False

    'Gestisci potenziale errore in K10
    On Error Resume Next
    dataGiorno9 = DateValue(Worksheets("Elabora Giornaliera").Range("K10").Value)
    On Error GoTo 0

    'Controlla se la conversione della data è fallita
    If IsDate(dataGiorno9) Then
        ' Ciclo attraverso le righe del foglio di origine
        For i = 1 To ultimaRiga
            ' Controlla se la riga è vuota
            If IsEmpty(wsOrigine.Cells(i, 1).Value) Then Exit For

            On Error Resume Next
            data = CDate(Trim(wsOrigine.Cells(i, 1).Value))
            On Error GoTo 0

            ' Controlla se la data è uguale a dataGiorno9
            If data = dataGiorno9 Then
                almenoUnaCorrispondenza = True
                ' Verifica se riga destinazione non è 21 o 23
                If rigaDestinazione <> 21 And rigaDestinazione <> 23 Then
                    ' Copia i valori
                    wsDestinazione.Cells(rigaDestinazione, 1).Value = wsOrigine.Cells(i, 2).Value
                    wsDestinazione.Cells(rigaDestinazione, 4).Value = wsOrigine.Cells(i, 5).Value
                    wsDestinazione.Cells(rigaDestinazione, 5).Value = wsOrigine.Cells(i, 6).Value
                End If

                ' Aggiungi valori a A24 e U24, gestendo errori di conversione
                valoreC = Trim(wsOrigine.Cells(i, 3).Value)
                If Not IsEmpty(valoreC) Then
                    If Not ValoreEsistente(valoriC, valoreC) Then
                        valoriC.Add valoreC
                        concatenatoA24 = concatenatoA24 & IIf(concatenatoA24 = "", "", vbCrLf) & valoreC
                    End If
                End If

                valoreD = Trim(wsOrigine.Cells(i, 4).Value)
                If Not IsEmpty(valoreD) Then
                    If Not ValoreEsistente(valoriD, valoreD) Then
                        valoriD.Add valoreD
                        concatenatoU24 = concatenatoU24 & IIf(concatenatoU24 = "", "", vbCrLf) & valoreD
                    End If
                End If

                rigaDestinazione = rigaDestinazione + 1
            End If
        Next i

        ' Assegna le concatenazioni alle celle A24 e U24
        wsDestinazione.Range("A24").Value = concatenatoA24
        wsDestinazione.Range("U24").Value = concatenatoU24
    Else
        MsgBox "La cella K10 del foglio 'Elabora Giornaliera' non contiene una data valida.", vbExclamation
    End If

    Application.CutCopyMode = False
    Set valoriC = Nothing
    Set valoriD = Nothing
    Set wsOrigine = Nothing
    Set wsDestinazione = Nothing

End Sub

Function ValoreEsistente(valori As Collection, valore As String) As Boolean
    Dim v As Variant
    On Error Resume Next
    For Each v In valori
        If v = valore Then
            ValoreEsistente = True
            Exit Function
        End If
    Next v
    ValoreEsistente = False
End Function


```

## Componente: Foglio2.cls
Stream: VBA/Foglio2

```vba
Attribute VB_Name = "Foglio2"
Attribute VB_Base = "0{00020820-0000-0000-C000-000000000046}"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Attribute VB_TemplateDerived = False
Attribute VB_Customizable = True

```

## Componente: Modulo2.bas
Stream: VBA/Modulo2

```vba
Attribute VB_Name = "Modulo2"
Sub InviaEmailConsuntivoChiamata()
    On Error GoTo ErrorHandler

    ' Dichiarazione delle variabili
    Dim wb As Workbook
    Dim wsData As Worksheet
    Dim wsConsuntivo As Worksheet
    Dim wsRifVBA As Worksheet
    Dim tbl As ListObject
    Dim tblNome As ListObject
    Dim tempWb As Workbook
    Dim tempWs As Worksheet
    Dim rng As Range
    Dim cell As Range
    Dim shp As Shape
    Dim OutlookApp As Object
    Dim OutlookMail As Object
    Dim filePath As String
    Dim destinatario As String
    Dim cc As String
    Dim OGGETTO As String
    Dim nomeDestinatario As String
    Dim emailCercata As String
    Dim trovatoNome As Boolean
    Dim corpoEmail As String
    Dim i As Long
    Dim errCell As String
    Dim avviso As String
    Dim odc As String


    ' Verifica se la cella A22 del foglio "Consuntivo" contiene qualcosa
    With ThisWorkbook.Sheets("Consuntivo")
        If Trim(.Range("A22").Value) = "" Then
            MsgBox "Il consuntivo risulta vuoto.", vbExclamation
            Exit Sub 'Esci dalla subroutine se la cella è vuota
        End If

        ' Nuove verifiche per celle vuote
        If .Range("J10").Value = "INSERIRE DATA" Then
            MsgBox "Inserisci data.", vbExclamation
            Exit Sub
        End If
        If .Range("D14").Value = "INSERISCI DESCRIZIONE LAVORO" Then
            MsgBox "Inserisci descrizione lavoro.", vbExclamation
            Exit Sub
        End If
        If .Range("J14").Value = "INSERIRE N°CONS." Then
            MsgBox "Inserisci n°consuntivo o verifica formato nome file.", vbExclamation
            Exit Sub
        End If
        If .Range("B56").Value = "INSERIRE PERSONA" Then
            MsgBox "Inserisci Persona che compila il consuntivo.", vbExclamation
            Exit Sub
        End If
        If .Range("H12").Value = "INSERIRE ASSISTENTE" Then
            MsgBox "Inserisci Assistente TCL.", vbExclamation
            Exit Sub
        End If

    End With


    ' Imposta la tua cartella di lavoro attiva
    Set wb = ThisWorkbook
    Set wsData = wb.Sheets("Inserimento Dati")
    Set wsConsuntivo = wb.Sheets("Consuntivo")
    Set wsRifVBA = wb.Sheets("rif.VBA")

    ' Prendi la Tabella6
    On Error Resume Next
    Set tbl = wsData.ListObjects("Tabella6")
    On Error GoTo 0

    ' Verifica se la Tabella6 esiste
    If tbl Is Nothing Then
        MsgBox "La Tabella6 non è stata trovata nel foglio 'Inserimento Dati'."
        Exit Sub
    End If

    ' Ottieni la Tabella9
    On Error Resume Next
    Set tblNome = wsData.ListObjects("Tabella9")
    On Error GoTo 0

    If tblNome Is Nothing Then
        MsgBox "La Tabella9 non è stata trovata."
        Exit Sub
    End If

    ' Blocco dei riferimenti alle celle - Foglio "rif.VBA"
    With wsRifVBA
        OGGETTO = " Chiamata di reperibilità - cons." & .Range("A4").Value & " del " & Format(.Range("A6").Value, "dd-mm-yyyy")
        emailCercata = Trim(.Range("J13").Value)

        ' Gestione Avviso e ODC  - Migliorata gestione errori
        On Error Resume Next
        If Len(Trim(.Range("B6").Value)) > 0 Then
            avviso = " AVVISO " & .Range("B6").Value
        Else
            avviso = ""
        End If
        If Len(Trim(.Range("C6").Value)) > 0 Then
            odc = " ODC " & .Range("C6").Value
        Else
            odc = ""
        End If
        On Error GoTo 0

        OGGETTO = OGGETTO & avviso & odc

    End With

    ' Sostituisci caratteri non validi nel nome del file
    OGGETTO = Replace(OGGETTO, "\", "-")
    OGGETTO = Replace(OGGETTO, "/", "-")
    OGGETTO = Replace(OGGETTO, ":", "-")
    OGGETTO = Replace(OGGETTO, "*", "-")
    OGGETTO = Replace(OGGETTO, "?", "-")
    OGGETTO = Replace(OGGETTO, """", "-")
    OGGETTO = Replace(OGGETTO, "<", "-")
    OGGETTO = Replace(OGGETTO, ">", "-")
    OGGETTO = Replace(OGGETTO, "|", "-")

    ' Concatenazione dei destinatari con gestione errori
    destinatario = ""
    cc = ""
    For i = 1 To tbl.ListRows.Count
        On Error Resume Next
        destinatario = destinatario & ";" & CStr(tbl.ListColumns("DESTINATARIO").DataBodyRange.Cells(i, 1).Value)
        If Err.Number <> 0 Then
            errCell = "DESTINATARIO, riga " & i
            Err.Clear
        End If
        cc = cc & ";" & CStr(tbl.ListColumns("IN CC").DataBodyRange.Cells(i, 1).Value)
        If Err.Number <> 0 Then
            errCell = "IN CC, riga " & i
            Err.Clear
        End If
        On Error GoTo 0
    Next i

    If errCell <> "" Then
        MsgBox "Errore nella colonna " & errCell
        Exit Sub
    End If

    'Elimina il primo punto e virgola
    destinatario = Mid(destinatario, 2)
    cc = Mid(cc, 2)


    ' Ricerca del nome
    trovatoNome = False
    For i = 1 To tblNome.ListRows.Count
        If Trim(tblNome.ListColumns("Email").DataBodyRange.Cells(i, 1).Value) = emailCercata Then
            nomeDestinatario = tblNome.ListColumns("Nome").DataBodyRange.Cells(i, 1).Value
            trovatoNome = True
            Exit For
        End If
    Next i

    If Not trovatoNome Then
        MsgBox "Nessun nome trovato per l'email in F28: " & emailCercata
        Exit Sub
    End If

    ' Crea un nuovo file Excel temporaneo
    Set tempWb = Workbooks.Add
    Set tempWs = tempWb.Sheets(1)

    ' Copia l'intervallo da A3 a L63 nel nuovo file e trasforma formule in valori
    Set rng = wsConsuntivo.Range("A3:L63")
    rng.Copy
    With tempWs.Range("A1")
        .PasteSpecial Paste:=xlPasteValues
        .PasteSpecial Paste:=xlPasteFormats
    End With

    ' Imposta la larghezza delle colonne e l'altezza delle righe
    For Each cell In rng.Cells
        tempWs.Columns(cell.Column - rng.Column + 1).ColumnWidth = wsConsuntivo.Columns(cell.Column).ColumnWidth
        tempWs.Rows(cell.Row - rng.Row + 1).RowHeight = wsConsuntivo.Rows(cell.Row).RowHeight
    Next cell

    ' Copia tutte le immagini
    For Each shp In wsConsuntivo.Shapes
        If Not Intersect(shp.TopLeftCell, rng) Is Nothing Then
            shp.Copy
            tempWs.Paste Destination:=tempWs.Cells(shp.TopLeftCell.Row - rng.Row + 1, shp.TopLeftCell.Column - rng.Column + 1)
        End If
    Next shp

    ' Salva il file temporaneo con il nome aggiornato
    filePath = Environ("TEMP") & "\" & OGGETTO & ".xlsx"
    tempWb.SaveAs filePath
    tempWb.Close False

    ' Verifica se il file è stato creato correttamente
    If filePath = "" Then
        MsgBox "Il file non è stato creato correttamente."
        Exit Sub
    End If

    ' Crea un nuovo oggetto Outlook
    Set OutlookApp = CreateObject("Outlook.Application")
    Set OutlookMail = OutlookApp.CreateItem(0)

    ' Crea il corpo dell'email
    corpoEmail = "<p><span style='font-size:16px;'><b><i>Gent.mo " & nomeDestinatario & ",</i></b></span></p>" & _
                 "<p>Con la presente invio in allegato <b>Consuntivo n° " & wsRifVBA.Range("A4").Value & "</b> " & _
                 "insieme alla relazione tecnica correlata, " & _
                 "preparata a seguito della chiamata di reperibilità effettuata in data <b>" & _
                 wsRifVBA.Range("A6").Value & "</b> riguardante:</p>"

    'Aggiunta informazioni al corpoEmail da A11 ad A15
    For i = 8 To 12
        If wsRifVBA.Cells(i, 1).Value <> "" Then
            corpoEmail = corpoEmail & "<p><b>• " & wsRifVBA.Cells(i, 1).Value & "</b></p>"
        End If
    Next i

    corpoEmail = corpoEmail & "<p>Rimango in attesa di ODC e ti ringrazio, come sempre, per la celerità.</p>" & _
                 "<p><span style='font-size:16px;'><b><i>Saluti,</i></b></span></p>" & GetOutlookSignature()

    ' Imposta i dettagli dell'email
    With OutlookMail
        .To = destinatario
        .cc = cc
        .Subject = OGGETTO
        .HTMLBody = corpoEmail
        If Dir(filePath) <> "" Then .Attachments.Add filePath
        .Display ' Usa .Send per inviare direttamente senza visualizzarla
    End With

    ' Pulisci
    Set OutlookMail = Nothing
    Set OutlookApp = Nothing
    Set tempWb = Nothing
    Set tempWs = Nothing
    Set rng = Nothing
    Set cell = Nothing
    Set shp = Nothing
    Set tbl = Nothing
    Set tblNome = Nothing
    Exit Sub

ErrorHandler:
    MsgBox "Si è verificato un errore: " & Err.Description & " in riga: " & Erl
End Sub

Function GetOutlookSignature() As String
    Dim objOutlook As Object
    Dim objMail As Object
    Dim objInspector As Object

    On Error Resume Next
    Set objOutlook = CreateObject("Outlook.Application")
    Set objMail = objOutlook.CreateItem(0)
    Set objInspector = objMail.GetInspector
    GetOutlookSignature = objMail.HTMLBody
    On Error GoTo 0

    Set objMail = Nothing
    Set objOutlook = Nothing
End Function



```

## Componente: Modulo4.bas
Stream: VBA/Modulo4

```vba
Attribute VB_Name = "Modulo4"
Option Explicit

Sub InviaEmailGenerico()
    On Error GoTo ErrorHandler

    ' --- VARIABILI ---
    Dim OutlookApp As Object, OutlookMail As Object
    Dim wb As Workbook, tempWb As Workbook
    Dim wsData As Worksheet, wsRifVBA As Worksheet, wsConsuntivo As Worksheet, tempWs As Worksheet
    Dim tbl As ListObject, tblNome As ListObject
    Dim rng As Range, cell As Range, shp As Shape
    Dim rngOggetto As Range, rngEmailCercata As Range, rngDataRiferimento As Range
    Dim rngDataCompilazione As Range, rngInterventi As Range, rngTipoEmail As Range

    Dim filePath As String, nomeFileTemp As String
    Dim destinatario As String, cc As String, OGGETTO As String
    Dim nomeDestinatario As String, cognomeDestinatario As String, emailCercata As String
    Dim corpoEmail As String, firma As String
    Dim i As Long, trovatoNome As Boolean

    ' --- INIZIALIZZAZIONE ---
    Set wb = ThisWorkbook
    Set wsData = wb.Sheets("Inserimento Dati")
    Set wsRifVBA = wb.Sheets("rif.VBA")
    Set wsConsuntivo = wb.Sheets("Consuntivo")

    ' --- RIFERIMENTI ---
    With wsData
        On Error Resume Next
        Set tbl = .ListObjects("Tabella612")
        Set tblNome = .ListObjects("Tabella9")
        On Error GoTo ErrorHandler
    End With

    If tbl Is Nothing Or tblNome Is Nothing Then
        MsgBox "Errore Critico: Tabelle dati mancanti.", vbCritical
        Exit Sub
    End If

    With wsRifVBA
        Set rngOggetto = .Range("L3")
        Set rngEmailCercata = .Range("J3")
        Set rngDataRiferimento = .Range("A4")
        Set rngDataCompilazione = .Range("A6")
        Set rngInterventi = .Range("A8:A18")
        Set rngTipoEmail = .Range("F19")
    End With

    ' --- DESTINATARI ---
    destinatario = ""
    cc = ""
    If tbl.ListRows.Count > 0 Then
        For i = 1 To tbl.ListRows.Count
            Dim dest As String, copia As String
            dest = tbl.ListColumns("DESTINATARIO").DataBodyRange.Cells(i, 1).Value
            copia = tbl.ListColumns("IN CC").DataBodyRange.Cells(i, 1).Value
            If dest <> "" Then destinatario = destinatario & IIf(destinatario = "", "", ";") & dest
            If copia <> "" Then cc = cc & IIf(cc = "", "", ";") & copia
        Next i
    End If

    ' --- RICERCA NOME ---
    OGGETTO = rngOggetto.Value
    emailCercata = Trim(rngEmailCercata.Value)
    trovatoNome = False

    For i = 1 To tblNome.ListRows.Count
        If Trim(tblNome.ListColumns("Email").DataBodyRange.Cells(i, 1).Value) = emailCercata Then
            nomeDestinatario = tblNome.ListColumns("Nome").DataBodyRange.Cells(i, 1).Value
            cognomeDestinatario = tblNome.ListColumns("Cognome").DataBodyRange.Cells(i, 1).Value
            trovatoNome = True
            Exit For
        End If
    Next i

    If Not trovatoNome Then
        MsgBox "Nome non trovato per: " & emailCercata, vbExclamation
        Exit Sub
    End If

    ' --- FILE TEMP ---
    Application.ScreenUpdating = False
    Set tempWb = Workbooks.Add
    Set tempWs = tempWb.Sheets(1)
    Set rng = wsConsuntivo.Range("A3:L63")
    rng.Copy
    With tempWs.Range("A1")
        .PasteSpecial Paste:=xlPasteColumnWidths
        .PasteSpecial Paste:=xlPasteValues
        .PasteSpecial Paste:=xlPasteFormats
    End With
    For i = 1 To rng.Rows.Count
        tempWs.Rows(i).RowHeight = wsConsuntivo.Rows(rng.Row + i - 1).RowHeight
    Next i
    For Each shp In wsConsuntivo.Shapes
        If Not Intersect(shp.TopLeftCell, rng) Is Nothing Then
            shp.Copy
            tempWs.Paste Destination:=tempWs.Cells(shp.TopLeftCell.Row - rng.Row + 1, shp.TopLeftCell.Column - rng.Column + 1)
        End If
    Next shp

    nomeFileTemp = CleanFileName(OGGETTO)
    nomeFileTemp = Left(nomeFileTemp, 100)
    filePath = Environ("TEMP") & "\" & nomeFileTemp & ".xlsx"

    On Error Resume Next
    Application.DisplayAlerts = False
    tempWb.SaveAs filePath
    If Err.Number <> 0 Then
        MsgBox "Errore Salvataggio: " & Err.Description, vbCritical
        tempWb.Close False: Application.ScreenUpdating = True: Exit Sub
    End If
    Application.DisplayAlerts = True
    On Error GoTo ErrorHandler
    tempWb.Close False
    Application.ScreenUpdating = True

    ' --- BODY EMAIL (FIX DEFINITIVO FONT E SPAZIATURA) ---
    Set OutlookApp = CreateObject("Outlook.Application")
    Set OutlookMail = OutlookApp.CreateItem(0)

    ' Visualizziamo subito per caricare la firma HTML corretta nativa di Outlook
    OutlookMail.Display
    firma = OutlookMail.HTMLBody ' Cattura la firma e gli stili predefiniti

    Dim dataRif As String, dataComp As String
    dataRif = rngDataRiferimento.Value
    If IsDate(rngDataCompilazione.Value) Then dataComp = Format(rngDataCompilazione.Value, "dd/mm/yyyy") Else dataComp = rngDataCompilazione.Value

    Dim stlCell As String
    ' Aggiunto margin:0 per eliminare spaziature paragrafo e mso-line-height-rule per fissare l'altezza
    stlCell = "font-family:'Calibri',sans-serif; font-size:11pt; color:#000000; padding:0; margin:0;"

    ' START TABELLA
    ' Aggiunto border-collapse:collapse per eliminare spazi tra celle
    corpoEmail = "<table border='0' cellspacing='0' cellpadding='0' style='width:100%; border-collapse:collapse; font-family:''Calibri'',sans-serif; font-size:11pt;'>"

    ' 1. SALUTI
    corpoEmail = corpoEmail & "<tr><td style='" & stlCell & "'>"
    If UCase(rngTipoEmail.Value) = "FORMALE" Then
        corpoEmail = corpoEmail & "<b><i>Gent.mo Sig. " & nomeDestinatario & " " & cognomeDestinatario & ",</i></b>"
    Else
        corpoEmail = corpoEmail & "<b><i>Gent.mo " & nomeDestinatario & ",</i></b>"
    End If
    corpoEmail = corpoEmail & "</td></tr>"

    ' 2. SPAZIO (15pt)
    corpoEmail = corpoEmail & "<tr><td style='height:15pt; font-size:1pt; line-height:1pt;'>&nbsp;</td></tr>"

    ' 3. TESTO INTRODUTTIVO
    corpoEmail = corpoEmail & "<tr><td style='" & stlCell & "'>"
    If UCase(rngTipoEmail.Value) = "FORMALE" Then
        corpoEmail = corpoEmail & "Con la presente desidero trasmettere in allegato il Consuntivo n° <b>" & dataRif & "</b> datato <b>" & dataComp & "</b> relativo ai seguenti interventi:"
    Else
        corpoEmail = corpoEmail & "Con la presente, invio in allegato <b>Consuntivo n° " & dataRif & "</b> in data <b>" & dataComp & "</b> riguardante:"
    End If
    corpoEmail = corpoEmail & "</td></tr>"

    ' 4. SPAZIO (10pt)
    corpoEmail = corpoEmail & "<tr><td style='height:10pt; font-size:1pt; line-height:1pt;'>&nbsp;</td></tr>"

    ' 5. ELENCO INTERVENTI
    corpoEmail = corpoEmail & "<tr><td><table border='0' cellspacing='0' cellpadding='0' style='border-collapse:collapse;'>"
    For Each cell In rngInterventi
        If Trim(cell.Value) <> "" Then
            corpoEmail = corpoEmail & "<tr>"
            corpoEmail = corpoEmail & "<td width='20' style='width:20pt;'></td>"
            corpoEmail = corpoEmail & "<td valign='top' style='" & stlCell & " width:10pt;'>&bull;</td>"
            corpoEmail = corpoEmail & "<td style='" & stlCell & "'><b>" & cell.Value & "</b></td>"
            corpoEmail = corpoEmail & "</tr>"
            corpoEmail = corpoEmail & "<tr><td colspan='3' style='height:3pt; font-size:1pt; line-height:1pt;'>&nbsp;</td></tr>"
        End If
    Next cell
    corpoEmail = corpoEmail & "</table></td></tr>"

    ' 6. SPAZIO (10pt)
    corpoEmail = corpoEmail & "<tr><td style='height:10pt; font-size:1pt; line-height:1pt;'>&nbsp;</td></tr>"

    ' 7. CHIUSURA
    corpoEmail = corpoEmail & "<tr><td style='" & stlCell & "'>"
    If UCase(rngTipoEmail.Value) = "FORMALE" Then
        corpoEmail = corpoEmail & "Resto in attesa dell'ODC e ringrazio, come sempre, per la vostra disponibilità."
    Else
        corpoEmail = corpoEmail & "Rimango in attesa di ODC e ti ringrazio sempre per la celerità."
    End If
    corpoEmail = corpoEmail & "</td></tr>"

    ' 8. SPAZIO (15pt) e SALUTI FINALI
    corpoEmail = corpoEmail & "<tr><td style='height:15pt; font-size:1pt; line-height:1pt;'>&nbsp;</td></tr>"
    corpoEmail = corpoEmail & "<tr><td style='" & stlCell & "'><b><i>Saluti,</i></b></td></tr>"

    ' END TABELLA (Nessun <br> extra aggiunto qui per evitare doppio spazio prima della firma)
    corpoEmail = corpoEmail & "</table>"

    With OutlookMail
        .To = destinatario
        .cc = cc
        .Subject = OGGETTO
        ' Unione pulita: Tabella + Firma Originale (senza rompere l'HTML)
        .HTMLBody = corpoEmail & firma
        .Attachments.Add filePath
        ' .Display non necessario chiamarlo di nuovo, ma utile per portare in primo piano
    End With

    Set tempWb = Nothing: Set tempWs = Nothing: Set wb = Nothing
    Set OutlookMail = Nothing: Set OutlookApp = Nothing
    Exit Sub

ErrorHandler:
    Application.ScreenUpdating = True
    MsgBox "Errore Imprevisto: " & Err.Number & " - " & Err.Description, vbCritical
End Sub

Function CleanFileName(s As String) As String
    Dim invalidChars As String: Dim i As Integer
    invalidChars = "/\:*?""<>|": CleanFileName = s
    For i = 1 To Len(invalidChars)
        CleanFileName = Replace(CleanFileName, Mid(invalidChars, i, 1), "_")
    Next i
End Function

```

## Componente: Modulo5.bas
Stream: VBA/Modulo5

```vba
Attribute VB_Name = "Modulo5"
Option Explicit

Sub CreaEConvertiRelazioneTecnica()

    Dim wdApp As Object, wdDoc As Object
    Dim titolo As String, OGGETTO As String, CORPO As String, tecnico As String
    Dim progressivo As String, data As String, consuntivoNum As String, fileName As String, fileNameClean As String
    Dim filePath As String, folderPath As String, pdfPath As String, rootPath As String
    Dim fso As Object, fileCount As Integer
    Dim annoShort As String, annoLong As String
    Dim rngTitolo As Range, rngOggetto As Range, rngCorpo As Range, rngTecnico As Range
    Dim rngConsuntivoNum As Range, rngData As Range, rngNumACapo As Range
    Dim numACapo As Integer, i As Integer

    ' --- INIZIALIZZAZIONE FSO ---
    Set fso = CreateObject("Scripting.FileSystemObject")

    ' Riferimenti alle celle del foglio "rif.VBA"
    With ThisWorkbook.Sheets("rif.VBA")
        Set rngTitolo = .Range("F4")
        Set rngOggetto = .Range("F6")
        Set rngCorpo = .Range("F8")
        Set rngTecnico = .Range("F13")
        Set rngConsuntivoNum = .Range("A4")
        Set rngData = .Range("A6")
        Set rngNumACapo = .Range("H19")
    End With

    ' Assegna i valori delle celle a variabili
    titolo = rngTitolo.Value
    OGGETTO = rngOggetto.Value
    CORPO = rngCorpo.Value
    tecnico = rngTecnico.Value
    data = Format(rngData.Value, "DD/MM/YYYY")
    consuntivoNum = rngConsuntivoNum.Value
    numACapo = rngNumACapo.Value

    ' --- GESTIONE DINAMICA DATE E PERCORSI ---
    annoLong = CStr(Year(rngData.Value))
    annoShort = Right(annoLong, 2)

    ' Percorso base fisso
    rootPath = "\\192.168.11.251\Database_Tecnico_SMI\Contabilita' strumentale\Relazioni di reperibilita'\"

    ' Costruzione percorsi dinamici
    folderPath = rootPath & annoLong & "\WORD"
    pdfPath = rootPath & annoLong & "\PDF"

    ' Verifica e Creazione Cartelle
    If Not fso.FolderExists(rootPath & annoLong) Then
        On Error Resume Next
        fso.CreateFolder rootPath & annoLong
        On Error GoTo 0
    End If

    If Not fso.FolderExists(folderPath) Then
        On Error Resume Next
        fso.CreateFolder folderPath
        On Error GoTo 0
    End If

    If Not fso.FolderExists(pdfPath) Then
        On Error Resume Next
        fso.CreateFolder pdfPath
        On Error GoTo 0
    End If

    If Not fso.FolderExists(folderPath) Or Not fso.FolderExists(pdfPath) Then
        MsgBox "Impossibile raggiungere o creare il percorso di rete:" & vbCrLf & rootPath & annoLong, vbCritical
        Exit Sub
    End If

    ' --- WORD AUTOMATION ---
    Set wdApp = CreateObject("Word.Application")
    wdApp.Visible = True
    Set wdDoc = wdApp.Documents.Add

    ' Calcola il numero di file esistenti nella cartella WORD
    fileCount = 0
    On Error Resume Next
    fileCount = fso.GetFolder(folderPath).Files.Count
    On Error GoTo 0

    ' Calcola il progressivo
    progressivo = Format(fileCount + 1, "000")

    ' Genera nomi file
    fileNameClean = CleanFileName(progressivo & "-" & annoShort & " - relazione tecnica per cons. " & consuntivoNum & " datato " & data)
    fileName = fileNameClean & ".docx"
    filePath = folderPath & "\" & fileName

    ' Contenuto Word
    With wdDoc.Content
        .Font.Name = "Lora"
        .Font.Size = 20
        .ParagraphFormat.Alignment = 3 ' Giustificato
        .InsertAfter titolo & vbCrLf & vbCrLf & OGGETTO & vbCrLf & vbCrLf & CORPO
        For i = 1 To numACapo
            .InsertAfter vbCrLf
        Next i
        .InsertAfter "Priolo Gargallo " & data & Space(12) & "Il Tecnico Strumentista" & vbCrLf & Space(64) & tecnico
    End With

    ' Salva Word
    On Error Resume Next
    wdDoc.SaveAs2 filePath
    If Err.Number <> 0 Then
        MsgBox "Errore nel salvataggio Word: " & Err.Description, vbCritical
        wdDoc.Close False: wdApp.Quit: Exit Sub
    End If
    On Error GoTo 0

    ' Salva PDF
    Dim pdfFullFilePath As String
    pdfFullFilePath = pdfPath & "\" & fileNameClean & ".pdf"

    On Error Resume Next
    wdDoc.SaveAs2 pdfFullFilePath, 17
    On Error GoTo 0

    ' Chiudi tutto
    wdDoc.Close SaveChanges:=False
    wdApp.Quit

    ' --- APERTURA CARTELLE ---
    ' Apre le due cartelle in Esplora Risorse
    ' Le virgolette triple servono a gestire eventuali spazi nei percorsi
    Shell "explorer.exe """ & folderPath & """", vbNormalFocus
    Shell "explorer.exe """ & pdfPath & """", vbNormalFocus

    ' Rilascia oggetti
    Set wdDoc = Nothing: Set wdApp = Nothing: Set fso = Nothing
    Set rngTitolo = Nothing: Set rngOggetto = Nothing: Set rngCorpo = Nothing
    Set rngTecnico = Nothing: Set rngConsuntivoNum = Nothing
    Set rngData = Nothing: Set rngNumACapo = Nothing

End Sub

Function CleanFileName(ByVal fileName As String) As String
    Dim i As Long
    Dim invalidChars As String
    invalidChars = "\/:*?""<>|"
    For i = 1 To Len(invalidChars)
        fileName = Replace(fileName, Mid(invalidChars, i, 1), "_")
    Next i
    CleanFileName = fileName
End Function


```

## Componente: Modulo6.bas
Stream: VBA/Modulo6

```vba
Attribute VB_Name = "Modulo6"
Sub NascondiScopriRighe()
    Dim rng As Range
    Set rng = Rows("26:41") ' Intervallo da nascondere/scoprire

    If rng.EntireRow.Hidden Then
        rng.EntireRow.Hidden = False ' Scopri le righe
    Else
        rng.EntireRow.Hidden = True ' Nascondi le righe
    End If
End Sub


```

## Componente: Modulo7.bas
Stream: VBA/Modulo7

```vba
Attribute VB_Name = "Modulo7"
Private Sub Workbook_Open()
    Dim nomeFile As String
    Dim numeroProgressivo As String

    ' Ottiene il nome del file senza estensione e percorso
    nomeFile = ThisWorkbook.Name

    ' Prende i primi 6 caratteri del nome del file
    If Len(nomeFile) >= 6 Then
        numeroProgressivo = Left(nomeFile, 6) ' Estrae i primi 6 caratteri
        ' Sostituisce il trattino con la barra
        numeroProgressivo = Replace(numeroProgressivo, "-", "/")

        ' Verifica se il formato è corretto
        If Not IsFormatCorretto(numeroProgressivo) Then
            MsgBox "Errore: il formato del numero progressivo deve essere '000/00'.", vbCritical, "Formato Errato"
        Else
            ' Inserisce il numero progressivo in A4 nel foglio 'rif.VBA'
            ThisWorkbook.Sheets("rif.VBA").Range("A4").Value = numeroProgressivo
        End If
    Else
        MsgBox "Formato Errato: il nome del file non contiene abbastanza caratteri.", vbCritical, "Errore"
    End If
    Call AggiornaFestiviAnnuali
End Sub

Function IsFormatCorretto(ByVal numero As String) As Boolean
    ' Verifica se il numero è nel formato '000/00'
    Dim regex As Object
    Set regex = CreateObject("VBScript.RegExp")

    With regex
        .Pattern = "^\d{3}/\d{2}$" ' Regex per '000/00'
        .IgnoreCase = True
        .Global = False
    End With

    IsFormatCorretto = regex.Test(numero)
End Function

Sub Auto_Open()
    Call Workbook_Open
End Sub

```

## Componente: Foglio9.cls
Stream: VBA/Foglio9

```vba
Attribute VB_Name = "Foglio9"
Attribute VB_Base = "0{00020820-0000-0000-C000-000000000046}"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Attribute VB_TemplateDerived = False
Attribute VB_Customizable = True

```

## Componente: Foglio10.cls
Stream: VBA/Foglio10

```vba
Attribute VB_Name = "Foglio10"
Attribute VB_Base = "0{00020820-0000-0000-C000-000000000046}"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Attribute VB_TemplateDerived = False
Attribute VB_Customizable = True

```

## Componente: Foglio11.cls
Stream: VBA/Foglio11

```vba
Attribute VB_Name = "Foglio11"
Attribute VB_Base = "0{00020820-0000-0000-C000-000000000046}"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Attribute VB_TemplateDerived = False
Attribute VB_Customizable = True

```

## Componente: Modulo3.bas
Stream: VBA/Modulo3

```vba
Attribute VB_Name = "Modulo3"
Sub CaricaDatiMultiplo()
    Dim wbDest As Workbook
    Dim wsDest As Worksheet
    Dim percorsoFile As String
    Dim tabella As ListObject
    Dim errore As String
    Dim fileAperto As Boolean
    Dim ultimaRigaConteggio As Long
    Dim i As Long
    Dim righeNonVuoto As Long
    Dim datiFiltrati As Range
    Dim numeroConsuntivo As Variant
    Dim wsCaricaGiornaliera As Worksheet

    Dim rigaPerIncollare As Long
    Dim primoBloccoIncollato As Boolean

    Dim rigaLoopComandi As Long
    Dim abilitaPercorso As String
    Dim wbCheck As Workbook
    Dim errNumSalvataggio As Long

    ' Variabili per ottimizzazione velocità
    Dim prevScreenUpdating As Boolean
    Dim prevEnableEvents As Boolean
    Dim prevCalculation As XlCalculation

    ' --- Inizio Ottimizzazione Velocità ---
    prevScreenUpdating = Application.ScreenUpdating
    prevEnableEvents = Application.EnableEvents
    prevCalculation = Application.Calculation

    Application.ScreenUpdating = False
    Application.EnableEvents = False
    Application.Calculation = xlCalculationManual
    Application.StatusBar = "Avvio elaborazione..." ' Messaggio iniziale nella barra di stato

    On Error GoTo GestoreErroriGenerali ' Imposta gestore errori generale PRIMA di operazioni critiche

    '--- Recupero del valore per il filtro "Consuntivo" ---
    numeroConsuntivo = ThisWorkbook.Sheets("rif.VBA").Range("A4").Value

    '--- Impostazione e pulizia del foglio "Carica_Giornaliera" ---
    Set wsCaricaGiornaliera = ThisWorkbook.Sheets("Carica_Giornaliera")
    wsCaricaGiornaliera.Range("A1:N2000").ClearContents ' Considera se questo range è sempre sufficiente

    primoBloccoIncollato = False

    '--- Ciclo per ogni riga nel foglio "Comandi" (da 2 a 13 ORA) ---
    For rigaLoopComandi = 2 To 13 ' MODIFICATO: Esteso fino alla riga 13
        ' Aggiorna il messaggio della barra di stato per riflettere il nuovo totale (13-2+1 = 12 file)
        Application.StatusBar = "Controllo file " & (rigaLoopComandi - 1) & " di 12... Percorso: " & percorsoFile

        Set wbDest = Nothing
        Set wsDest = Nothing
        Set tabella = Nothing
        Set datiFiltrati = Nothing
        fileAperto = False
        errore = ""

        percorsoFile = Trim(CStr(ThisWorkbook.Sheets("Comandi").Cells(rigaLoopComandi, "A").Value))
        abilitaPercorso = UCase(Trim(CStr(ThisWorkbook.Sheets("Comandi").Cells(rigaLoopComandi, "R").Value)))

        If percorsoFile = "" Or abilitaPercorso <> "SI" Then
            Application.StatusBar = "File saltato (percorso vuoto o non abilitato): Riga " & rigaLoopComandi & " del foglio Comandi."
            GoTo ProssimoFile
        End If

        Application.StatusBar = "Elaborazione file: " & percorsoFile

        On Error GoTo GestoreErroriFileCorrente

        For Each wbCheck In Workbooks
            If wbCheck.FullName = percorsoFile Then
                Set wbDest = wbCheck
                fileAperto = True
                Exit For
            End If
        Next wbCheck

        If Not fileAperto Then
            If Dir(percorsoFile) <> "" Then
                Set wbDest = Workbooks.Open(percorsoFile, ReadOnly:=True, UpdateLinks:=0)
            Else
                Application.StatusBar = "File non trovato (saltato): " & percorsoFile
                GoTo ProssimoFile
            End If
        End If

        If wbDest Is Nothing Then
            Application.StatusBar = "Impossibile accedere al file (wbDest is Nothing, saltato): " & percorsoFile
            GoTo ProssimoFile
        End If

        Set wsDest = wbDest.Sheets("RIASSUNTO")
        Set tabella = wsDest.ListObjects("Tabella4")

        If tabella.AutoFilter.FilterMode Then
            tabella.AutoFilter.ShowAllData
        End If
        tabella.Range.AutoFilter Field:=13, Criteria1:=numeroConsuntivo

        On Error Resume Next
        Set datiFiltrati = tabella.DataBodyRange.SpecialCells(xlCellTypeVisible)
        errNumSalvataggio = Err.Number
        On Error GoTo GestoreErroriFileCorrente

        If errNumSalvataggio = 1004 Then
            Err.Clear
            Application.StatusBar = "Nessun dato visibile dopo filtro per il file: " & percorsoFile
        ElseIf errNumSalvataggio <> 0 Then
            Err.Raise errNumSalvataggio, "CaricaDatiMultiplo", "Errore durante SpecialCells nel file: " & percorsoFile
        End If

        If Not datiFiltrati Is Nothing Then
            If datiFiltrati.Rows.Count > 0 Then
                If Not primoBloccoIncollato Then
                    rigaPerIncollare = 1
                Else
                    rigaPerIncollare = wsCaricaGiornaliera.Cells(wsCaricaGiornaliera.Rows.Count, "A").End(xlUp).Row
                    If rigaPerIncollare = 1 And IsEmpty(wsCaricaGiornaliera.Cells(1, "A").Value) Then
                        rigaPerIncollare = 1
                    Else
                        rigaPerIncollare = rigaPerIncollare + 1
                    End If
                End If
                Application.StatusBar = "Copia dati da " & percorsoFile & " a riga " & rigaPerIncollare & "..."
                datiFiltrati.Copy
                wsCaricaGiornaliera.Cells(rigaPerIncollare, 1).PasteSpecial xlPasteValues
                Application.CutCopyMode = False
                primoBloccoIncollato = True
            Else
                Application.StatusBar = "datiFiltrati valido ma con 0 righe nel file: " & percorsoFile
            End If
        End If

PuliziaFileCorrente:
        If Not fileAperto And Not wbDest Is Nothing Then
            wbDest.Close SaveChanges:=False
        End If
        Set wbDest = Nothing
        Set wsDest = Nothing
        Set tabella = Nothing
        Set datiFiltrati = Nothing
        fileAperto = False

        On Error GoTo 0
        GoTo ProssimoFile

GestoreErroriFileCorrente:
    errore = "Errore (" & Err.Number & "): " & Err.Description & " nel file: " & percorsoFile & ". Salto al prossimo."
    Application.StatusBar = errore
    Err.Clear
    GoTo PuliziaFileCorrente

ProssimoFile:
    Next rigaLoopComandi

    On Error GoTo GestoreErroriGenerali

    Application.StatusBar = "Conteggio righe caricate..."
    ultimaRigaConteggio = wsCaricaGiornaliera.Cells(wsCaricaGiornaliera.Rows.Count, "A").End(xlUp).Row
    righeNonVuoto = 0
    If ultimaRigaConteggio >= 1 Then
        For i = 1 To ultimaRigaConteggio
            If Trim(CStr(wsCaricaGiornaliera.Cells(i, "A").Value)) <> "" Then
                righeNonVuoto = righeNonVuoto + 1
            End If
        Next i
    End If

    ThisWorkbook.Sheets("Elabora Giornaliera").Range("I1").Value = righeNonVuoto

    Application.StatusBar = "Elaborazione completata. Righe caricate: " & righeNonVuoto & ". Pronto."

    GoTo RipristinaImpostazioniExcel

GestoreErroriGenerali:
    If Err.Number <> 0 Then
        errore = "Errore generale (" & Err.Number & "): " & Err.Description
        If percorsoFile <> "" Then
             errore = errore & " (ultimo file: " & percorsoFile & ")"
        End If
        MsgBox errore, vbCritical, "Errore Macro CaricaDatiMultiplo"
        Application.StatusBar = errore
    ElseIf Len(errore) > 0 Then
        MsgBox errore, vbCritical, "Errore Macro CaricaDatiMultiplo"
        Application.StatusBar = errore
    End If

    If Not IsMissing(fileAperto) Then
        If Not fileAperto And Not wbDest Is Nothing Then
            On Error Resume Next
            wbDest.Close SaveChanges:=False
            On Error GoTo 0
        End If
    End If

RipristinaImpostazioniExcel:
    Application.ScreenUpdating = prevScreenUpdating
    Application.EnableEvents = prevEnableEvents
    Application.Calculation = prevCalculation
    If Application.StatusBar <> False And InStr(Application.StatusBar, "Elaborazione completata") = 0 And InStr(Application.StatusBar, "Errore") = 0 Then
        Application.StatusBar = False
    End If
End Sub



```

## Componente: Modulo8.bas
Stream: VBA/Modulo8

```vba
Attribute VB_Name = "Modulo8"
Sub elaboraDati()

    Dim ws As Worksheet
    Dim lastRow As Long
    Dim i As Long
    Dim numRows As Long ' Manteniamo Long come nel codice originale

    Set ws = ThisWorkbook.Sheets("Elabora Giornaliera")

    ' Cancella le righe non vuote da A2 in poi
    ' Aggiunto un controllo per evitare errori se ci sono meno di 2 righe con dati
    If ws.Cells(ws.Rows.Count, "A").End(xlUp).Row >= 2 Then
        lastRow = ws.Cells(ws.Rows.Count, "A").End(xlUp).Row
        For i = lastRow To 2 Step -1
            If ws.Cells(i, "A").Value <> "" Then
                ws.Rows(i).EntireRow.Delete
            End If
        Next i
    End If

    ' Ottieni il numero di righe da copiare da I1
    On Error Resume Next ' Gestione errore se I1 è vuoto o non numerico
    numRows = 0 ' Inizializza numRows a 0. Se I1 è testo/vuoto, numRows rimarrà 0.
    numRows = ws.Range("I1").Value
    On Error GoTo 0 ' Ripristina gestione errori standard

    ' Controlla se il valore in I1 è ESPLICITAMENTE un numero negativo.
    ' Se I1 è vuoto, testo, o 0, questa condizione non sarà vera.
    If IsNumeric(ws.Range("I1").Value) And ws.Range("I1").Value < 0 Then
        MsgBox "Il valore in I1 (" & ws.Range("I1").Value & ") non può essere un numero negativo.", vbExclamation
        Exit Sub ' Esce dalla Sub solo se il numero è effettivamente negativo
    End If

    ' Copia le formule solo se numRows è strettamente maggiore di 0.
    ' Se numRows è 0 (perché I1 era 0, vuoto o testo), questa parte viene saltata
    ' e non viene mostrato nessun messaggio.
    If numRows > 0 Then
        ws.Range("A1:G1").AutoFill Destination:=ws.Range("A1:G" & numRows)
    End If

    ' Queste chiamate verranno eseguite sempre, a meno che Exit Sub non sia stato
    ' chiamato sopra a causa di un valore negativo in I1.
    Call CancellaColonnaKDaK2
    Call CancellaColonnaLDaL2
    Call caricaPDL
    Call EstraiDateUnivoche
    Call EstraiValoriUnivociDaColonnaL
End Sub



```

## Componente: Modulo19.bas
Stream: VBA/Modulo19

```vba
Attribute VB_Name = "Modulo19"
Sub SmistaDatiGiorno11()
    Dim wsOrigine As Worksheet, wsDestinazione As Worksheet
    Dim ultimaRiga As Long, i As Long
    Dim data As Date, dataGiorno11 As Date
    Dim rigaDestinazione As Long
    Dim concatenatoA24 As String
    Dim concatenatoU24 As String
    Dim valoreC As String
    Dim valoreD As String
    Dim valoriC As Collection
    Dim valoriD As Collection
    Dim almenoUnaCorrispondenza As Boolean

    ' Imposta i fogli
    Set wsOrigine = ThisWorkbook.Sheets("Elabora Giornaliera")
    Set wsDestinazione = ThisWorkbook.Sheets("11")

    ' Trova l'ultima riga con dati nel foglio di origine
    ultimaRiga = wsOrigine.Cells(Rows.Count, 1).End(xlUp).Row

    ' Inizializza la riga di partenza per le colonne
    rigaDestinazione = 11

    ' Inizializza le celle di destinazione A24 e U24
    concatenatoA24 = ""
    concatenatoU24 = ""

    ' Inizializza le collezioni per rimuovere duplicati
    Set valoriC = New Collection
    Set valoriD = New Collection

    almenoUnaCorrispondenza = False

    'Gestisci potenziale errore in K12
    On Error Resume Next
    dataGiorno11 = DateValue(Worksheets("Elabora Giornaliera").Range("K12").Value)
    On Error GoTo 0

    'Controlla se la conversione della data è fallita
    If IsDate(dataGiorno11) Then
        ' Ciclo attraverso le righe del foglio di origine
        For i = 1 To ultimaRiga
            ' Controlla se la riga è vuota
            If IsEmpty(wsOrigine.Cells(i, 1).Value) Then Exit For

            On Error Resume Next
            data = CDate(Trim(wsOrigine.Cells(i, 1).Value))
            On Error GoTo 0

            ' Controlla se la data è uguale a dataGiorno11
            If data = dataGiorno11 Then
                almenoUnaCorrispondenza = True
                ' Verifica se riga destinazione non è 21 o 23
                If rigaDestinazione <> 21 And rigaDestinazione <> 23 Then
                    ' Copia i valori
                    wsDestinazione.Cells(rigaDestinazione, 1).Value = wsOrigine.Cells(i, 2).Value
                    wsDestinazione.Cells(rigaDestinazione, 4).Value = wsOrigine.Cells(i, 5).Value
                    wsDestinazione.Cells(rigaDestinazione, 5).Value = wsOrigine.Cells(i, 6).Value
                End If

                ' Aggiungi valori a A24 e U24, gestendo errori di conversione
                valoreC = Trim(wsOrigine.Cells(i, 3).Value)
                If Not IsEmpty(valoreC) Then
                    If Not ValoreEsistente(valoriC, valoreC) Then
                        valoriC.Add valoreC
                        concatenatoA24 = concatenatoA24 & IIf(concatenatoA24 = "", "", vbCrLf) & valoreC
                    End If
                End If

                valoreD = Trim(wsOrigine.Cells(i, 4).Value)
                If Not IsEmpty(valoreD) Then
                    If Not ValoreEsistente(valoriD, valoreD) Then
                        valoriD.Add valoreD
                        concatenatoU24 = concatenatoU24 & IIf(concatenatoU24 = "", "", vbCrLf) & valoreD
                    End If
                End If

                rigaDestinazione = rigaDestinazione + 1
            End If
        Next i

        ' Assegna le concatenazioni alle celle A24 e U24
        wsDestinazione.Range("A24").Value = concatenatoA24
        wsDestinazione.Range("U24").Value = concatenatoU24
    Else
        MsgBox "La cella K12 del foglio 'Elabora Giornaliera' non contiene una data valida.", vbExclamation
    End If

    Application.CutCopyMode = False
    Set valoriC = Nothing
    Set valoriD = Nothing
    Set wsOrigine = Nothing
    Set wsDestinazione = Nothing

End Sub

Function ValoreEsistente(valori As Collection, valore As String) As Boolean
    Dim v As Variant
    On Error Resume Next
    For Each v In valori
        If v = valore Then
            ValoreEsistente = True
            Exit Function
        End If
    Next v
    ValoreEsistente = False
End Function


```

## Componente: Modulo20.bas
Stream: VBA/Modulo20

```vba
Attribute VB_Name = "Modulo20"
Sub SmistaDatiGiorno12()
    Dim wsOrigine As Worksheet, wsDestinazione As Worksheet
    Dim ultimaRiga As Long, i As Long
    Dim data As Date, dataGiorno12 As Date
    Dim rigaDestinazione As Long
    Dim concatenatoA24 As String
    Dim concatenatoU24 As String
    Dim valoreC As String
    Dim valoreD As String
    Dim valoriC As Collection
    Dim valoriD As Collection
    Dim almenoUnaCorrispondenza As Boolean

    ' Imposta i fogli
    Set wsOrigine = ThisWorkbook.Sheets("Elabora Giornaliera")
    Set wsDestinazione = ThisWorkbook.Sheets("12")

    ' Trova l'ultima riga con dati nel foglio di origine
    ultimaRiga = wsOrigine.Cells(Rows.Count, 1).End(xlUp).Row

    ' Inizializza la riga di partenza per le colonne
    rigaDestinazione = 11

    ' Inizializza le celle di destinazione A24 e U24
    concatenatoA24 = ""
    concatenatoU24 = ""

    ' Inizializza le collezioni per rimuovere duplicati
    Set valoriC = New Collection
    Set valoriD = New Collection

    almenoUnaCorrispondenza = False

    'Gestisci potenziale errore in K13
    On Error Resume Next
    dataGiorno12 = DateValue(Worksheets("Elabora Giornaliera").Range("K13").Value)
    On Error GoTo 0

    'Controlla se la conversione della data è fallita
    If IsDate(dataGiorno12) Then
        ' Ciclo attraverso le righe del foglio di origine
        For i = 1 To ultimaRiga
            ' Controlla se la riga è vuota
            If IsEmpty(wsOrigine.Cells(i, 1).Value) Then Exit For

            On Error Resume Next
            data = CDate(Trim(wsOrigine.Cells(i, 1).Value))
            On Error GoTo 0

            ' Controlla se la data è uguale a dataGiorno12
            If data = dataGiorno12 Then
                almenoUnaCorrispondenza = True
                ' Verifica se riga destinazione non è 21 o 23
                If rigaDestinazione <> 21 And rigaDestinazione <> 23 Then
                    ' Copia i valori
                    wsDestinazione.Cells(rigaDestinazione, 1).Value = wsOrigine.Cells(i, 2).Value
                    wsDestinazione.Cells(rigaDestinazione, 4).Value = wsOrigine.Cells(i, 5).Value
                    wsDestinazione.Cells(rigaDestinazione, 5).Value = wsOrigine.Cells(i, 6).Value
                End If

                ' Aggiungi valori a A24 e U24, gestendo errori di conversione
                valoreC = Trim(wsOrigine.Cells(i, 3).Value)
                If Not IsEmpty(valoreC) Then
                    If Not ValoreEsistente(valoriC, valoreC) Then
                        valoriC.Add valoreC
                        concatenatoA24 = concatenatoA24 & IIf(concatenatoA24 = "", "", vbCrLf) & valoreC
                    End If
                End If

                valoreD = Trim(wsOrigine.Cells(i, 4).Value)
                If Not IsEmpty(valoreD) Then
                    If Not ValoreEsistente(valoriD, valoreD) Then
                        valoriD.Add valoreD
                        concatenatoU24 = concatenatoU24 & IIf(concatenatoU24 = "", "", vbCrLf) & valoreD
                    End If
                End If

                rigaDestinazione = rigaDestinazione + 1
            End If
        Next i

        ' Assegna le concatenazioni alle celle A24 e U24
        wsDestinazione.Range("A24").Value = concatenatoA24
        wsDestinazione.Range("U24").Value = concatenatoU24
    Else
        MsgBox "La cella K13 del foglio 'Elabora Giornaliera' non contiene una data valida.", vbExclamation
    End If

    Application.CutCopyMode = False
    Set valoriC = Nothing
    Set valoriD = Nothing
    Set wsOrigine = Nothing
    Set wsDestinazione = Nothing

End Sub

Function ValoreEsistente(valori As Collection, valore As String) As Boolean
    Dim v As Variant
    On Error Resume Next
    For Each v In valori
        If v = valore Then
            ValoreEsistente = True
            Exit Function
        End If
    Next v
    ValoreEsistente = False
End Function


```

## Componente: Modulo21.bas
Stream: VBA/Modulo21

```vba
Attribute VB_Name = "Modulo21"
Sub SmistaDatiGiorno13()
    Dim wsOrigine As Worksheet, wsDestinazione As Worksheet
    Dim ultimaRiga As Long, i As Long
    Dim data As Date, dataGiorno13 As Date
    Dim rigaDestinazione As Long
    Dim concatenatoA24 As String
    Dim concatenatoU24 As String
    Dim valoreC As String
    Dim valoreD As String
    Dim valoriC As Collection
    Dim valoriD As Collection
    Dim almenoUnaCorrispondenza As Boolean

    ' Imposta i fogli
    Set wsOrigine = ThisWorkbook.Sheets("Elabora Giornaliera")
    Set wsDestinazione = ThisWorkbook.Sheets("13")

    ' Trova l'ultima riga con dati nel foglio di origine
    ultimaRiga = wsOrigine.Cells(Rows.Count, 1).End(xlUp).Row

    ' Inizializza la riga di partenza per le colonne
    rigaDestinazione = 11

    ' Inizializza le celle di destinazione A24 e U24
    concatenatoA24 = ""
    concatenatoU24 = ""

    ' Inizializza le collezioni per rimuovere duplicati
    Set valoriC = New Collection
    Set valoriD = New Collection

    almenoUnaCorrispondenza = False

    'Gestisci potenziale errore in K14
    On Error Resume Next
    dataGiorno13 = DateValue(Worksheets("Elabora Giornaliera").Range("K14").Value)
    On Error GoTo 0

    'Controlla se la conversione della data è fallita
    If IsDate(dataGiorno13) Then
        ' Ciclo attraverso le righe del foglio di origine
        For i = 1 To ultimaRiga
            ' Controlla se la riga è vuota
            If IsEmpty(wsOrigine.Cells(i, 1).Value) Then Exit For

            On Error Resume Next
            data = CDate(Trim(wsOrigine.Cells(i, 1).Value))
            On Error GoTo 0

            ' Controlla se la data è uguale a dataGiorno13
            If data = dataGiorno13 Then
                almenoUnaCorrispondenza = True
                ' Verifica se riga destinazione non è 21 o 23
                If rigaDestinazione <> 21 And rigaDestinazione <> 23 Then
                    ' Copia i valori
                    wsDestinazione.Cells(rigaDestinazione, 1).Value = wsOrigine.Cells(i, 2).Value
                    wsDestinazione.Cells(rigaDestinazione, 4).Value = wsOrigine.Cells(i, 5).Value
                    wsDestinazione.Cells(rigaDestinazione, 5).Value = wsOrigine.Cells(i, 6).Value
                End If

                ' Aggiungi valori a A24 e U24, gestendo errori di conversione
                valoreC = Trim(wsOrigine.Cells(i, 3).Value)
                If Not IsEmpty(valoreC) Then
                    If Not ValoreEsistente(valoriC, valoreC) Then
                        valoriC.Add valoreC
                        concatenatoA24 = concatenatoA24 & IIf(concatenatoA24 = "", "", vbCrLf) & valoreC
                    End If
                End If

                valoreD = Trim(wsOrigine.Cells(i, 4).Value)
                If Not IsEmpty(valoreD) Then
                    If Not ValoreEsistente(valoriD, valoreD) Then
                        valoriD.Add valoreD
                        concatenatoU24 = concatenatoU24 & IIf(concatenatoU24 = "", "", vbCrLf) & valoreD
                    End If
                End If

                rigaDestinazione = rigaDestinazione + 1
            End If
        Next i

        ' Assegna le concatenazioni alle celle A24 e U24
        wsDestinazione.Range("A24").Value = concatenatoA24
        wsDestinazione.Range("U24").Value = concatenatoU24
    Else
        MsgBox "La cella K14 del foglio 'Elabora Giornaliera' non contiene una data valida.", vbExclamation
    End If

    Application.CutCopyMode = False
    Set valoriC = Nothing
    Set valoriD = Nothing
    Set wsOrigine = Nothing
    Set wsDestinazione = Nothing

End Sub

Function ValoreEsistente(valori As Collection, valore As String) As Boolean
    Dim v As Variant
    On Error Resume Next
    For Each v In valori
        If v = valore Then
            ValoreEsistente = True
            Exit Function
        End If
    Next v
    ValoreEsistente = False
End Function


```

## Componente: Modulo22.bas
Stream: VBA/Modulo22

```vba
Attribute VB_Name = "Modulo22"
Sub SmistaDatiGiorno14()
    Dim wsOrigine As Worksheet, wsDestinazione As Worksheet
    Dim ultimaRiga As Long, i As Long
    Dim data As Date, dataGiorno14 As Date
    Dim rigaDestinazione As Long
    Dim concatenatoA24 As String
    Dim concatenatoU24 As String
    Dim valoreC As String
    Dim valoreD As String
    Dim valoriC As Collection
    Dim valoriD As Collection
    Dim almenoUnaCorrispondenza As Boolean

    ' Imposta i fogli
    Set wsOrigine = ThisWorkbook.Sheets("Elabora Giornaliera")
    Set wsDestinazione = ThisWorkbook.Sheets("14")

    ' Trova l'ultima riga con dati nel foglio di origine
    ultimaRiga = wsOrigine.Cells(Rows.Count, 1).End(xlUp).Row

    ' Inizializza la riga di partenza per le colonne
    rigaDestinazione = 11

    ' Inizializza le celle di destinazione A24 e U24
    concatenatoA24 = ""
    concatenatoU24 = ""

    ' Inizializza le collezioni per rimuovere duplicati
    Set valoriC = New Collection
    Set valoriD = New Collection

    almenoUnaCorrispondenza = False

    'Gestisci potenziale errore in K15
    On Error Resume Next
    dataGiorno14 = DateValue(Worksheets("Elabora Giornaliera").Range("K15").Value)
    On Error GoTo 0

    'Controlla se la conversione della data è fallita
    If IsDate(dataGiorno14) Then
        ' Ciclo attraverso le righe del foglio di origine
        For i = 1 To ultimaRiga
            ' Controlla se la riga è vuota
            If IsEmpty(wsOrigine.Cells(i, 1).Value) Then Exit For

            On Error Resume Next
            data = CDate(Trim(wsOrigine.Cells(i, 1).Value))
            On Error GoTo 0

            ' Controlla se la data è uguale a dataGiorno14
            If data = dataGiorno14 Then
                almenoUnaCorrispondenza = True
                ' Verifica se riga destinazione non è 21 o 23
                If rigaDestinazione <> 21 And rigaDestinazione <> 23 Then
                    ' Copia i valori
                    wsDestinazione.Cells(rigaDestinazione, 1).Value = wsOrigine.Cells(i, 2).Value
                    wsDestinazione.Cells(rigaDestinazione, 4).Value = wsOrigine.Cells(i, 5).Value
                    wsDestinazione.Cells(rigaDestinazione, 5).Value = wsOrigine.Cells(i, 6).Value
                End If

                ' Aggiungi valori a A24 e U24, gestendo errori di conversione
                valoreC = Trim(wsOrigine.Cells(i, 3).Value)
                If Not IsEmpty(valoreC) Then
                    If Not ValoreEsistente(valoriC, valoreC) Then
                        valoriC.Add valoreC
                        concatenatoA24 = concatenatoA24 & IIf(concatenatoA24 = "", "", vbCrLf) & valoreC
                    End If
                End If

                valoreD = Trim(wsOrigine.Cells(i, 4).Value)
                If Not IsEmpty(valoreD) Then
                    If Not ValoreEsistente(valoriD, valoreD) Then
                        valoriD.Add valoreD
                        concatenatoU24 = concatenatoU24 & IIf(concatenatoU24 = "", "", vbCrLf) & valoreD
                    End If
                End If

                rigaDestinazione = rigaDestinazione + 1
            End If
        Next i

        ' Assegna le concatenazioni alle celle A24 e U24
        wsDestinazione.Range("A24").Value = concatenatoA24
        wsDestinazione.Range("U24").Value = concatenatoU24
    Else
        MsgBox "La cella K15 del foglio 'Elabora Giornaliera' non contiene una data valida.", vbExclamation
    End If

    Application.CutCopyMode = False
    Set valoriC = Nothing
    Set valoriD = Nothing
    Set wsOrigine = Nothing
    Set wsDestinazione = Nothing

End Sub

Function ValoreEsistente(valori As Collection, valore As String) As Boolean
    Dim v As Variant
    On Error Resume Next
    For Each v In valori
        If v = valore Then
            ValoreEsistente = True
            Exit Function
        End If
    Next v
    ValoreEsistente = False
End Function


```

## Componente: Modulo23.bas
Stream: VBA/Modulo23

```vba
Attribute VB_Name = "Modulo23"
Sub SmistaDatiGiorno15()
    Dim wsOrigine As Worksheet, wsDestinazione As Worksheet
    Dim ultimaRiga As Long, i As Long
    Dim data As Date, dataGiorno15 As Date
    Dim rigaDestinazione As Long
    Dim concatenatoA24 As String
    Dim concatenatoU24 As String
    Dim valoreC As String
    Dim valoreD As String
    Dim valoriC As Collection
    Dim valoriD As Collection
    Dim almenoUnaCorrispondenza As Boolean

    ' Imposta i fogli
    Set wsOrigine = ThisWorkbook.Sheets("Elabora Giornaliera")
    Set wsDestinazione = ThisWorkbook.Sheets("15")

    ' Trova l'ultima riga con dati nel foglio di origine
    ultimaRiga = wsOrigine.Cells(Rows.Count, 1).End(xlUp).Row

    ' Inizializza la riga di partenza per le colonne
    rigaDestinazione = 11

    ' Inizializza le celle di destinazione A24 e U24
    concatenatoA24 = ""
    concatenatoU24 = ""

    ' Inizializza le collezioni per rimuovere duplicati
    Set valoriC = New Collection
    Set valoriD = New Collection

    almenoUnaCorrispondenza = False

    'Gestisci potenziale errore in K16
    On Error Resume Next
    dataGiorno15 = DateValue(Worksheets("Elabora Giornaliera").Range("K16").Value)
    On Error GoTo 0

    'Controlla se la conversione della data è fallita
    If IsDate(dataGiorno15) Then
        ' Ciclo attraverso le righe del foglio di origine
        For i = 1 To ultimaRiga
            ' Controlla se la riga è vuota
            If IsEmpty(wsOrigine.Cells(i, 1).Value) Then Exit For

            On Error Resume Next
            data = CDate(Trim(wsOrigine.Cells(i, 1).Value))
            On Error GoTo 0

            ' Controlla se la data è uguale a dataGiorno15
            If data = dataGiorno15 Then
                almenoUnaCorrispondenza = True
                ' Verifica se riga destinazione non è 21 o 23
                If rigaDestinazione <> 21 And rigaDestinazione <> 23 Then
                    ' Copia i valori
                    wsDestinazione.Cells(rigaDestinazione, 1).Value = wsOrigine.Cells(i, 2).Value
                    wsDestinazione.Cells(rigaDestinazione, 4).Value = wsOrigine.Cells(i, 5).Value
                    wsDestinazione.Cells(rigaDestinazione, 5).Value = wsOrigine.Cells(i, 6).Value
                End If

                ' Aggiungi valori a A24 e U24, gestendo errori di conversione
                valoreC = Trim(wsOrigine.Cells(i, 3).Value)
                If Not IsEmpty(valoreC) Then
                    If Not ValoreEsistente(valoriC, valoreC) Then
                        valoriC.Add valoreC
                        concatenatoA24 = concatenatoA24 & IIf(concatenatoA24 = "", "", vbCrLf) & valoreC
                    End If
                End If

                valoreD = Trim(wsOrigine.Cells(i, 4).Value)
                If Not IsEmpty(valoreD) Then
                    If Not ValoreEsistente(valoriD, valoreD) Then
                        valoriD.Add valoreD
                        concatenatoU24 = concatenatoU24 & IIf(concatenatoU24 = "", "", vbCrLf) & valoreD
                    End If
                End If

                rigaDestinazione = rigaDestinazione + 1
            End If
        Next i

        ' Assegna le concatenazioni alle celle A24 e U24
        wsDestinazione.Range("A24").Value = concatenatoA24
        wsDestinazione.Range("U24").Value = concatenatoU24
    Else
        MsgBox "La cella K16 del foglio 'Elabora Giornaliera' non contiene una data valida.", vbExclamation
    End If

    Application.CutCopyMode = False
    Set valoriC = Nothing
    Set valoriD = Nothing
    Set wsOrigine = Nothing
    Set wsDestinazione = Nothing

End Sub

Function ValoreEsistente(valori As Collection, valore As String) As Boolean
    Dim v As Variant
    On Error Resume Next
    For Each v In valori
        If v = valore Then
            ValoreEsistente = True
            Exit Function
        End If
    Next v
    ValoreEsistente = False
End Function


```

## Componente: Modulo24.bas
Stream: VBA/Modulo24

```vba
Attribute VB_Name = "Modulo24"
Sub SmistaDatiGiorno16()
    Dim wsOrigine As Worksheet, wsDestinazione As Worksheet
    Dim ultimaRiga As Long, i As Long
    Dim data As Date, dataGiorno16 As Date
    Dim rigaDestinazione As Long
    Dim concatenatoA24 As String
    Dim concatenatoU24 As String
    Dim valoreC As String
    Dim valoreD As String
    Dim valoriC As Collection
    Dim valoriD As Collection
    Dim almenoUnaCorrispondenza As Boolean

    ' Imposta i fogli
    Set wsOrigine = ThisWorkbook.Sheets("Elabora Giornaliera")
    Set wsDestinazione = ThisWorkbook.Sheets("16")

    ' Trova l'ultima riga con dati nel foglio di origine
    ultimaRiga = wsOrigine.Cells(Rows.Count, 1).End(xlUp).Row

    ' Inizializza la riga di partenza per le colonne
    rigaDestinazione = 11

    ' Inizializza le celle di destinazione A24 e U24
    concatenatoA24 = ""
    concatenatoU24 = ""

    ' Inizializza le collezioni per rimuovere duplicati
    Set valoriC = New Collection
    Set valoriD = New Collection

    almenoUnaCorrispondenza = False

    'Gestisci potenziale errore in K17
    On Error Resume Next
    dataGiorno16 = DateValue(Worksheets("Elabora Giornaliera").Range("K17").Value)
    On Error GoTo 0

    'Controlla se la conversione della data è fallita
    If IsDate(dataGiorno16) Then
        ' Ciclo attraverso le righe del foglio di origine
        For i = 1 To ultimaRiga
            ' Controlla se la riga è vuota
            If IsEmpty(wsOrigine.Cells(i, 1).Value) Then Exit For

            On Error Resume Next
            data = CDate(Trim(wsOrigine.Cells(i, 1).Value))
            On Error GoTo 0

            ' Controlla se la data è uguale a dataGiorno16
            If data = dataGiorno16 Then
                almenoUnaCorrispondenza = True
                ' Verifica se riga destinazione non è 21 o 23
                If rigaDestinazione <> 21 And rigaDestinazione <> 23 Then
                    ' Copia i valori
                    wsDestinazione.Cells(rigaDestinazione, 1).Value = wsOrigine.Cells(i, 2).Value
                    wsDestinazione.Cells(rigaDestinazione, 4).Value = wsOrigine.Cells(i, 5).Value
                    wsDestinazione.Cells(rigaDestinazione, 5).Value = wsOrigine.Cells(i, 6).Value
                End If

                ' Aggiungi valori a A24 e U24, gestendo errori di conversione
                valoreC = Trim(wsOrigine.Cells(i, 3).Value)
                If Not IsEmpty(valoreC) Then
                    If Not ValoreEsistente(valoriC, valoreC) Then
                        valoriC.Add valoreC
                        concatenatoA24 = concatenatoA24 & IIf(concatenatoA24 = "", "", vbCrLf) & valoreC
                    End If
                End If

                valoreD = Trim(wsOrigine.Cells(i, 4).Value)
                If Not IsEmpty(valoreD) Then
                    If Not ValoreEsistente(valoriD, valoreD) Then
                        valoriD.Add valoreD
                        concatenatoU24 = concatenatoU24 & IIf(concatenatoU24 = "", "", vbCrLf) & valoreD
                    End If
                End If

                rigaDestinazione = rigaDestinazione + 1
            End If
        Next i

        ' Assegna le concatenazioni alle celle A24 e U24
        wsDestinazione.Range("A24").Value = concatenatoA24
        wsDestinazione.Range("U24").Value = concatenatoU24
    Else
        MsgBox "La cella K17 del foglio 'Elabora Giornaliera' non contiene una data valida.", vbExclamation
    End If

    Application.CutCopyMode = False
    Set valoriC = Nothing
    Set valoriD = Nothing
    Set wsOrigine = Nothing
    Set wsDestinazione = Nothing

End Sub

Function ValoreEsistente(valori As Collection, valore As String) As Boolean
    Dim v As Variant
    On Error Resume Next
    For Each v In valori
        If v = valore Then
            ValoreEsistente = True
            Exit Function
        End If
    Next v
    ValoreEsistente = False
End Function


```

## Componente: Modulo25.bas
Stream: VBA/Modulo25

```vba
Attribute VB_Name = "Modulo25"
Sub SmistaDatiGiorno17()
    Dim wsOrigine As Worksheet, wsDestinazione As Worksheet
    Dim ultimaRiga As Long, i As Long
    Dim data As Date, dataGiorno17 As Date
    Dim rigaDestinazione As Long
    Dim concatenatoA24 As String
    Dim concatenatoU24 As String
    Dim valoreC As String
    Dim valoreD As String
    Dim valoriC As Collection
    Dim valoriD As Collection
    Dim almenoUnaCorrispondenza As Boolean

    ' Imposta i fogli
    Set wsOrigine = ThisWorkbook.Sheets("Elabora Giornaliera")
    Set wsDestinazione = ThisWorkbook.Sheets("17")

    ' Trova l'ultima riga con dati nel foglio di origine
    ultimaRiga = wsOrigine.Cells(Rows.Count, 1).End(xlUp).Row

    ' Inizializza la riga di partenza per le colonne
    rigaDestinazione = 11

    ' Inizializza le celle di destinazione A24 e U24
    concatenatoA24 = ""
    concatenatoU24 = ""

    ' Inizializza le collezioni per rimuovere duplicati
    Set valoriC = New Collection
    Set valoriD = New Collection

    almenoUnaCorrispondenza = False

    'Gestisci potenziale errore in K18
    On Error Resume Next
    dataGiorno17 = DateValue(Worksheets("Elabora Giornaliera").Range("K18").Value)
    On Error GoTo 0

    'Controlla se la conversione della data è fallita
    If IsDate(dataGiorno17) Then
        ' Ciclo attraverso le righe del foglio di origine
        For i = 1 To ultimaRiga
            ' Controlla se la riga è vuota
            If IsEmpty(wsOrigine.Cells(i, 1).Value) Then Exit For

            On Error Resume Next
            data = CDate(Trim(wsOrigine.Cells(i, 1).Value))
            On Error GoTo 0

            ' Controlla se la data è uguale a dataGiorno17
            If data = dataGiorno17 Then
                almenoUnaCorrispondenza = True
                ' Verifica se riga destinazione non è 21 o 23
                If rigaDestinazione <> 21 And rigaDestinazione <> 23 Then
                    ' Copia i valori
                    wsDestinazione.Cells(rigaDestinazione, 1).Value = wsOrigine.Cells(i, 2).Value
                    wsDestinazione.Cells(rigaDestinazione, 4).Value = wsOrigine.Cells(i, 5).Value
                    wsDestinazione.Cells(rigaDestinazione, 5).Value = wsOrigine.Cells(i, 6).Value
                End If

                ' Aggiungi valori a A24 e U24, gestendo errori di conversione
                valoreC = Trim(wsOrigine.Cells(i, 3).Value)
                If Not IsEmpty(valoreC) Then
                    If Not ValoreEsistente(valoriC, valoreC) Then
                        valoriC.Add valoreC
                        concatenatoA24 = concatenatoA24 & IIf(concatenatoA24 = "", "", vbCrLf) & valoreC
                    End If
                End If

                valoreD = Trim(wsOrigine.Cells(i, 4).Value)
                If Not IsEmpty(valoreD) Then
                    If Not ValoreEsistente(valoriD, valoreD) Then
                        valoriD.Add valoreD
                        concatenatoU24 = concatenatoU24 & IIf(concatenatoU24 = "", "", vbCrLf) & valoreD
                    End If
                End If

                rigaDestinazione = rigaDestinazione + 1
            End If
        Next i

        ' Assegna le concatenazioni alle celle A24 e U24
        wsDestinazione.Range("A24").Value = concatenatoA24
        wsDestinazione.Range("U24").Value = concatenatoU24
    Else
        MsgBox "La cella K18 del foglio 'Elabora Giornaliera' non contiene una data valida.", vbExclamation
    End If

    Application.CutCopyMode = False
    Set valoriC = Nothing
    Set valoriD = Nothing
    Set wsOrigine = Nothing
    Set wsDestinazione = Nothing

End Sub

Function ValoreEsistente(valori As Collection, valore As String) As Boolean
    Dim v As Variant
    On Error Resume Next
    For Each v In valori
        If v = valore Then
            ValoreEsistente = True
            Exit Function
        End If
    Next v
    ValoreEsistente = False
End Function


```

## Componente: Modulo26.bas
Stream: VBA/Modulo26

```vba
Attribute VB_Name = "Modulo26"
Sub SmistaDatiGiorno18()
    Dim wsOrigine As Worksheet, wsDestinazione As Worksheet
    Dim ultimaRiga As Long, i As Long
    Dim data As Date, dataGiorno18 As Date
    Dim rigaDestinazione As Long
    Dim concatenatoA24 As String
    Dim concatenatoU24 As String
    Dim valoreC As String
    Dim valoreD As String
    Dim valoriC As Collection
    Dim valoriD As Collection
    Dim almenoUnaCorrispondenza As Boolean

    ' Imposta i fogli
    Set wsOrigine = ThisWorkbook.Sheets("Elabora Giornaliera")
    Set wsDestinazione = ThisWorkbook.Sheets("18")

    ' Trova l'ultima riga con dati nel foglio di origine
    ultimaRiga = wsOrigine.Cells(Rows.Count, 1).End(xlUp).Row

    ' Inizializza la riga di partenza per le colonne
    rigaDestinazione = 11

    ' Inizializza le celle di destinazione A24 e U24
    concatenatoA24 = ""
    concatenatoU24 = ""

    ' Inizializza le collezioni per rimuovere duplicati
    Set valoriC = New Collection
    Set valoriD = New Collection

    almenoUnaCorrispondenza = False

    'Gestisci potenziale errore in K19
    On Error Resume Next
    dataGiorno18 = DateValue(Worksheets("Elabora Giornaliera").Range("K19").Value)
    On Error GoTo 0

    'Controlla se la conversione della data è fallita
    If IsDate(dataGiorno18) Then
        ' Ciclo attraverso le righe del foglio di origine
        For i = 1 To ultimaRiga
            ' Controlla se la riga è vuota
            If IsEmpty(wsOrigine.Cells(i, 1).Value) Then Exit For

            On Error Resume Next
            data = CDate(Trim(wsOrigine.Cells(i, 1).Value))
            On Error GoTo 0

            ' Controlla se la data è uguale a dataGiorno18
            If data = dataGiorno18 Then
                almenoUnaCorrispondenza = True
                ' Verifica se riga destinazione non è 21 o 23
                If rigaDestinazione <> 21 And rigaDestinazione <> 23 Then
                    ' Copia i valori
                    wsDestinazione.Cells(rigaDestinazione, 1).Value = wsOrigine.Cells(i, 2).Value
                    wsDestinazione.Cells(rigaDestinazione, 4).Value = wsOrigine.Cells(i, 5).Value
                    wsDestinazione.Cells(rigaDestinazione, 5).Value = wsOrigine.Cells(i, 6).Value
                End If

                ' Aggiungi valori a A24 e U24, gestendo errori di conversione
                valoreC = Trim(wsOrigine.Cells(i, 3).Value)
                If Not IsEmpty(valoreC) Then
                    If Not ValoreEsistente(valoriC, valoreC) Then
                        valoriC.Add valoreC
                        concatenatoA24 = concatenatoA24 & IIf(concatenatoA24 = "", "", vbCrLf) & valoreC
                    End If
                End If

                valoreD = Trim(wsOrigine.Cells(i, 4).Value)
                If Not IsEmpty(valoreD) Then
                    If Not ValoreEsistente(valoriD, valoreD) Then
                        valoriD.Add valoreD
                        concatenatoU24 = concatenatoU24 & IIf(concatenatoU24 = "", "", vbCrLf) & valoreD
                    End If
                End If

                rigaDestinazione = rigaDestinazione + 1
            End If
        Next i

        ' Assegna le concatenazioni alle celle A24 e U24
        wsDestinazione.Range("A24").Value = concatenatoA24
        wsDestinazione.Range("U24").Value = concatenatoU24
    Else
        MsgBox "La cella K19 del foglio 'Elabora Giornaliera' non contiene una data valida.", vbExclamation
    End If

    Application.CutCopyMode = False
    Set valoriC = Nothing
    Set valoriD = Nothing
    Set wsOrigine = Nothing
    Set wsDestinazione = Nothing

End Sub

Function ValoreEsistente(valori As Collection, valore As String) As Boolean
    Dim v As Variant
    On Error Resume Next
    For Each v In valori
        If v = valore Then
            ValoreEsistente = True
            Exit Function
        End If
    Next v
    ValoreEsistente = False
End Function


```

## Componente: Modulo27.bas
Stream: VBA/Modulo27

```vba
Attribute VB_Name = "Modulo27"
Sub SmistaDatiGiorno19()
    Dim wsOrigine As Worksheet, wsDestinazione As Worksheet
    Dim ultimaRiga As Long, i As Long
    Dim data As Date, dataGiorno19 As Date
    Dim rigaDestinazione As Long
    Dim concatenatoA24 As String
    Dim concatenatoU24 As String
    Dim valoreC As String
    Dim valoreD As String
    Dim valoriC As Collection
    Dim valoriD As Collection
    Dim almenoUnaCorrispondenza As Boolean

    ' Imposta i fogli
    Set wsOrigine = ThisWorkbook.Sheets("Elabora Giornaliera")
    Set wsDestinazione = ThisWorkbook.Sheets("19")

    ' Trova l'ultima riga con dati nel foglio di origine
    ultimaRiga = wsOrigine.Cells(Rows.Count, 1).End(xlUp).Row

    ' Inizializza la riga di partenza per le colonne
    rigaDestinazione = 11

    ' Inizializza le celle di destinazione A24 e U24
    concatenatoA24 = ""
    concatenatoU24 = ""

    ' Inizializza le collezioni per rimuovere duplicati
    Set valoriC = New Collection
    Set valoriD = New Collection

    almenoUnaCorrispondenza = False

    'Gestisci potenziale errore in K20
    On Error Resume Next
    dataGiorno19 = DateValue(Worksheets("Elabora Giornaliera").Range("K20").Value)
    On Error GoTo 0

    'Controlla se la conversione della data è fallita
    If IsDate(dataGiorno19) Then
        ' Ciclo attraverso le righe del foglio di origine
        For i = 1 To ultimaRiga
            ' Controlla se la riga è vuota
            If IsEmpty(wsOrigine.Cells(i, 1).Value) Then Exit For

            On Error Resume Next
            data = CDate(Trim(wsOrigine.Cells(i, 1).Value))
            On Error GoTo 0

            ' Controlla se la data è uguale a dataGiorno19
            If data = dataGiorno19 Then
                almenoUnaCorrispondenza = True
                ' Verifica se riga destinazione non è 21 o 23
                If rigaDestinazione <> 21 And rigaDestinazione <> 23 Then
                    ' Copia i valori
                    wsDestinazione.Cells(rigaDestinazione, 1).Value = wsOrigine.Cells(i, 2).Value
                    wsDestinazione.Cells(rigaDestinazione, 4).Value = wsOrigine.Cells(i, 5).Value
                    wsDestinazione.Cells(rigaDestinazione, 5).Value = wsOrigine.Cells(i, 6).Value
                End If

                ' Aggiungi valori a A24 e U24, gestendo errori di conversione
                valoreC = Trim(wsOrigine.Cells(i, 3).Value)
                If Not IsEmpty(valoreC) Then
                    If Not ValoreEsistente(valoriC, valoreC) Then
                        valoriC.Add valoreC
                        concatenatoA24 = concatenatoA24 & IIf(concatenatoA24 = "", "", vbCrLf) & valoreC
                    End If
                End If

                valoreD = Trim(wsOrigine.Cells(i, 4).Value)
                If Not IsEmpty(valoreD) Then
                    If Not ValoreEsistente(valoriD, valoreD) Then
                        valoriD.Add valoreD
                        concatenatoU24 = concatenatoU24 & IIf(concatenatoU24 = "", "", vbCrLf) & valoreD
                    End If
                End If

                rigaDestinazione = rigaDestinazione + 1
            End If
        Next i

        ' Assegna le concatenazioni alle celle A24 e U24
        wsDestinazione.Range("A24").Value = concatenatoA24
        wsDestinazione.Range("U24").Value = concatenatoU24
    Else
        MsgBox "La cella K20 del foglio 'Elabora Giornaliera' non contiene una data valida.", vbExclamation
    End If

    Application.CutCopyMode = False
    Set valoriC = Nothing
    Set valoriD = Nothing
    Set wsOrigine = Nothing
    Set wsDestinazione = Nothing

End Sub

Function ValoreEsistente(valori As Collection, valore As String) As Boolean
    Dim v As Variant
    On Error Resume Next
    For Each v In valori
        If v = valore Then
            ValoreEsistente = True
            Exit Function
        End If
    Next v
    ValoreEsistente = False
End Function


```

## Componente: Modulo28.bas
Stream: VBA/Modulo28

```vba
Attribute VB_Name = "Modulo28"
Sub SmistaDatiGiorno20()
    Dim wsOrigine As Worksheet, wsDestinazione As Worksheet
    Dim ultimaRiga As Long, i As Long
    Dim data As Date, dataGiorno20 As Date
    Dim rigaDestinazione As Long
    Dim concatenatoA24 As String
    Dim concatenatoU24 As String
    Dim valoreC As String
    Dim valoreD As String
    Dim valoriC As Collection
    Dim valoriD As Collection
    Dim almenoUnaCorrispondenza As Boolean

    ' Imposta i fogli
    Set wsOrigine = ThisWorkbook.Sheets("Elabora Giornaliera")
    Set wsDestinazione = ThisWorkbook.Sheets("20")

    ' Trova l'ultima riga con dati nel foglio di origine
    ultimaRiga = wsOrigine.Cells(Rows.Count, 1).End(xlUp).Row

    ' Inizializza la riga di partenza per le colonne
    rigaDestinazione = 11

    ' Inizializza le celle di destinazione A24 e U24
    concatenatoA24 = ""
    concatenatoU24 = ""

    ' Inizializza le collezioni per rimuovere duplicati
    Set valoriC = New Collection
    Set valoriD = New Collection

    almenoUnaCorrispondenza = False

    'Gestisci potenziale errore in K21
    On Error Resume Next
    dataGiorno20 = DateValue(Worksheets("Elabora Giornaliera").Range("K21").Value)
    On Error GoTo 0

    'Controlla se la conversione della data è fallita
    If IsDate(dataGiorno20) Then
        ' Ciclo attraverso le righe del foglio di origine
        For i = 1 To ultimaRiga
            ' Controlla se la riga è vuota
            If IsEmpty(wsOrigine.Cells(i, 1).Value) Then Exit For

            On Error Resume Next
            data = CDate(Trim(wsOrigine.Cells(i, 1).Value))
            On Error GoTo 0

            ' Controlla se la data è uguale a dataGiorno20
            If data = dataGiorno20 Then
                almenoUnaCorrispondenza = True
                ' Verifica se riga destinazione non è 21 o 23
                If rigaDestinazione <> 21 And rigaDestinazione <> 23 Then
                    ' Copia i valori
                    wsDestinazione.Cells(rigaDestinazione, 1).Value = wsOrigine.Cells(i, 2).Value
                    wsDestinazione.Cells(rigaDestinazione, 4).Value = wsOrigine.Cells(i, 5).Value
                    wsDestinazione.Cells(rigaDestinazione, 5).Value = wsOrigine.Cells(i, 6).Value
                End If

                ' Aggiungi valori a A24 e U24, gestendo errori di conversione
                valoreC = Trim(wsOrigine.Cells(i, 3).Value)
                If Not IsEmpty(valoreC) Then
                    If Not ValoreEsistente(valoriC, valoreC) Then
                        valoriC.Add valoreC
                        concatenatoA24 = concatenatoA24 & IIf(concatenatoA24 = "", "", vbCrLf) & valoreC
                    End If
                End If

                valoreD = Trim(wsOrigine.Cells(i, 4).Value)
                If Not IsEmpty(valoreD) Then
                    If Not ValoreEsistente(valoriD, valoreD) Then
                        valoriD.Add valoreD
                        concatenatoU24 = concatenatoU24 & IIf(concatenatoU24 = "", "", vbCrLf) & valoreD
                    End If
                End If

                rigaDestinazione = rigaDestinazione + 1
            End If
        Next i

        ' Assegna le concatenazioni alle celle A24 e U24
        wsDestinazione.Range("A24").Value = concatenatoA24
        wsDestinazione.Range("U24").Value = concatenatoU24
    Else
        MsgBox "La cella K21 del foglio 'Elabora Giornaliera' non contiene una data valida.", vbExclamation
    End If

    Application.CutCopyMode = False
    Set valoriC = Nothing
    Set valoriD = Nothing
    Set wsOrigine = Nothing
    Set wsDestinazione = Nothing

End Sub

Function ValoreEsistente(valori As Collection, valore As String) As Boolean
    Dim v As Variant
    On Error Resume Next
    For Each v In valori
        If v = valore Then
            ValoreEsistente = True
            Exit Function
        End If
    Next v
    ValoreEsistente = False
End Function


```

## Componente: Modulo29.bas
Stream: VBA/Modulo29

```vba
Attribute VB_Name = "Modulo29"
Sub SmistaDatiGiorno21()
    Dim wsOrigine As Worksheet, wsDestinazione As Worksheet
    Dim ultimaRiga As Long, i As Long
    Dim data As Date, dataGiorno21 As Date
    Dim rigaDestinazione As Long
    Dim concatenatoA24 As String
    Dim concatenatoU24 As String
    Dim valoreC As String
    Dim valoreD As String
    Dim valoriC As Collection
    Dim valoriD As Collection
    Dim almenoUnaCorrispondenza As Boolean

    ' Imposta i fogli
    Set wsOrigine = ThisWorkbook.Sheets("Elabora Giornaliera")
    Set wsDestinazione = ThisWorkbook.Sheets("21")

    ' Trova l'ultima riga con dati nel foglio di origine
    ultimaRiga = wsOrigine.Cells(Rows.Count, 1).End(xlUp).Row

    ' Inizializza la riga di partenza per le colonne
    rigaDestinazione = 11

    ' Inizializza le celle di destinazione A24 e U24
    concatenatoA24 = ""
    concatenatoU24 = ""

    ' Inizializza le collezioni per rimuovere duplicati
    Set valoriC = New Collection
    Set valoriD = New Collection

    almenoUnaCorrispondenza = False

    'Gestisci potenziale errore in K22
    On Error Resume Next
    dataGiorno21 = DateValue(Worksheets("Elabora Giornaliera").Range("K22").Value)
    On Error GoTo 0

    'Controlla se la conversione della data è fallita
    If IsDate(dataGiorno21) Then
        ' Ciclo attraverso le righe del foglio di origine
        For i = 1 To ultimaRiga
            ' Controlla se la riga è vuota
            If IsEmpty(wsOrigine.Cells(i, 1).Value) Then Exit For

            On Error Resume Next
            data = CDate(Trim(wsOrigine.Cells(i, 1).Value))
            On Error GoTo 0

            ' Controlla se la data è uguale a dataGiorno21
            If data = dataGiorno21 Then
                almenoUnaCorrispondenza = True
                ' Verifica se riga destinazione non è 21 o 23
                If rigaDestinazione <> 21 And rigaDestinazione <> 23 Then
                    ' Copia i valori
                    wsDestinazione.Cells(rigaDestinazione, 1).Value = wsOrigine.Cells(i, 2).Value
                    wsDestinazione.Cells(rigaDestinazione, 4).Value = wsOrigine.Cells(i, 5).Value
                    wsDestinazione.Cells(rigaDestinazione, 5).Value = wsOrigine.Cells(i, 6).Value
                End If

                ' Aggiungi valori a A24 e U24, gestendo errori di conversione
                valoreC = Trim(wsOrigine.Cells(i, 3).Value)
                If Not IsEmpty(valoreC) Then
                    If Not ValoreEsistente(valoriC, valoreC) Then
                        valoriC.Add valoreC
                        concatenatoA24 = concatenatoA24 & IIf(concatenatoA24 = "", "", vbCrLf) & valoreC
                    End If
                End If

                valoreD = Trim(wsOrigine.Cells(i, 4).Value)
                If Not IsEmpty(valoreD) Then
                    If Not ValoreEsistente(valoriD, valoreD) Then
                        valoriD.Add valoreD
                        concatenatoU24 = concatenatoU24 & IIf(concatenatoU24 = "", "", vbCrLf) & valoreD
                    End If
                End If

                rigaDestinazione = rigaDestinazione + 1
            End If
        Next i

        ' Assegna le concatenazioni alle celle A24 e U24
        wsDestinazione.Range("A24").Value = concatenatoA24
        wsDestinazione.Range("U24").Value = concatenatoU24
    Else
        MsgBox "La cella K22 del foglio 'Elabora Giornaliera' non contiene una data valida.", vbExclamation
    End If

    Application.CutCopyMode = False
    Set valoriC = Nothing
    Set valoriD = Nothing
    Set wsOrigine = Nothing
    Set wsDestinazione = Nothing

End Sub

Function ValoreEsistente(valori As Collection, valore As String) As Boolean
    Dim v As Variant
    On Error Resume Next
    For Each v In valori
        If v = valore Then
            ValoreEsistente = True
            Exit Function
        End If
    Next v
    ValoreEsistente = False
End Function


```

## Componente: Modulo30.bas
Stream: VBA/Modulo30

```vba
Attribute VB_Name = "Modulo30"
Sub SmistaDatiGiorno22()
    Dim wsOrigine As Worksheet, wsDestinazione As Worksheet
    Dim ultimaRiga As Long, i As Long
    Dim data As Date, dataGiorno22 As Date
    Dim rigaDestinazione As Long
    Dim concatenatoA24 As String
    Dim concatenatoU24 As String
    Dim valoreC As String
    Dim valoreD As String
    Dim valoriC As Collection
    Dim valoriD As Collection
    Dim almenoUnaCorrispondenza As Boolean

    ' Imposta i fogli
    Set wsOrigine = ThisWorkbook.Sheets("Elabora Giornaliera")
    Set wsDestinazione = ThisWorkbook.Sheets("22")

    ' Trova l'ultima riga con dati nel foglio di origine
    ultimaRiga = wsOrigine.Cells(Rows.Count, 1).End(xlUp).Row

    ' Inizializza la riga di partenza per le colonne
    rigaDestinazione = 11

    ' Inizializza le celle di destinazione A24 e U24
    concatenatoA24 = ""
    concatenatoU24 = ""

    ' Inizializza le collezioni per rimuovere duplicati
    Set valoriC = New Collection
    Set valoriD = New Collection

    almenoUnaCorrispondenza = False

    'Gestisci potenziale errore in K23
    On Error Resume Next
    dataGiorno22 = DateValue(Worksheets("Elabora Giornaliera").Range("K23").Value)
    On Error GoTo 0

    'Controlla se la conversione della data è fallita
    If IsDate(dataGiorno22) Then
        ' Ciclo attraverso le righe del foglio di origine
        For i = 1 To ultimaRiga
            ' Controlla se la riga è vuota
            If IsEmpty(wsOrigine.Cells(i, 1).Value) Then Exit For

            On Error Resume Next
            data = CDate(Trim(wsOrigine.Cells(i, 1).Value))
            On Error GoTo 0

            ' Controlla se la data è uguale a dataGiorno22
            If data = dataGiorno22 Then
                almenoUnaCorrispondenza = True
                ' Verifica se riga destinazione non è 21 o 23
                If rigaDestinazione <> 21 And rigaDestinazione <> 23 Then
                    ' Copia i valori
                    wsDestinazione.Cells(rigaDestinazione, 1).Value = wsOrigine.Cells(i, 2).Value
                    wsDestinazione.Cells(rigaDestinazione, 4).Value = wsOrigine.Cells(i, 5).Value
                    wsDestinazione.Cells(rigaDestinazione, 5).Value = wsOrigine.Cells(i, 6).Value
                End If

                ' Aggiungi valori a A24 e U24, gestendo errori di conversione
                valoreC = Trim(wsOrigine.Cells(i, 3).Value)
                If Not IsEmpty(valoreC) Then
                    If Not ValoreEsistente(valoriC, valoreC) Then
                        valoriC.Add valoreC
                        concatenatoA24 = concatenatoA24 & IIf(concatenatoA24 = "", "", vbCrLf) & valoreC
                    End If
                End If

                valoreD = Trim(wsOrigine.Cells(i, 4).Value)
                If Not IsEmpty(valoreD) Then
                    If Not ValoreEsistente(valoriD, valoreD) Then
                        valoriD.Add valoreD
                        concatenatoU24 = concatenatoU24 & IIf(concatenatoU24 = "", "", vbCrLf) & valoreD
                    End If
                End If

                rigaDestinazione = rigaDestinazione + 1
            End If
        Next i

        ' Assegna le concatenazioni alle celle A24 e U24
        wsDestinazione.Range("A24").Value = concatenatoA24
        wsDestinazione.Range("U24").Value = concatenatoU24
    Else
        MsgBox "La cella K23 del foglio 'Elabora Giornaliera' non contiene una data valida.", vbExclamation
    End If

    Application.CutCopyMode = False
    Set valoriC = Nothing
    Set valoriD = Nothing
    Set wsOrigine = Nothing
    Set wsDestinazione = Nothing

End Sub

Function ValoreEsistente(valori As Collection, valore As String) As Boolean
    Dim v As Variant
    On Error Resume Next
    For Each v In valori
        If v = valore Then
            ValoreEsistente = True
            Exit Function
        End If
    Next v
    ValoreEsistente = False
End Function


```

## Componente: Modulo31.bas
Stream: VBA/Modulo31

```vba
Attribute VB_Name = "Modulo31"
Sub SmistaDatiGiorno23()
    Dim wsOrigine As Worksheet, wsDestinazione As Worksheet
    Dim ultimaRiga As Long, i As Long
    Dim data As Date, dataGiorno23 As Date
    Dim rigaDestinazione As Long
    Dim concatenatoA24 As String
    Dim concatenatoU24 As String
    Dim valoreC As String
    Dim valoreD As String
    Dim valoriC As Collection
    Dim valoriD As Collection
    Dim almenoUnaCorrispondenza As Boolean

    ' Imposta i fogli
    Set wsOrigine = ThisWorkbook.Sheets("Elabora Giornaliera")
    Set wsDestinazione = ThisWorkbook.Sheets("23")

    ' Trova l'ultima riga con dati nel foglio di origine
    ultimaRiga = wsOrigine.Cells(Rows.Count, 1).End(xlUp).Row

    ' Inizializza la riga di partenza per le colonne
    rigaDestinazione = 11

    ' Inizializza le celle di destinazione A24 e U24
    concatenatoA24 = ""
    concatenatoU24 = ""

    ' Inizializza le collezioni per rimuovere duplicati
    Set valoriC = New Collection
    Set valoriD = New Collection

    almenoUnaCorrispondenza = False

    'Gestisci potenziale errore in K24
    On Error Resume Next
    dataGiorno23 = DateValue(Worksheets("Elabora Giornaliera").Range("K24").Value)
    On Error GoTo 0

    'Controlla se la conversione della data è fallita
    If IsDate(dataGiorno23) Then
        ' Ciclo attraverso le righe del foglio di origine
        For i = 1 To ultimaRiga
            ' Controlla se la riga è vuota
            If IsEmpty(wsOrigine.Cells(i, 1).Value) Then Exit For

            On Error Resume Next
            data = CDate(Trim(wsOrigine.Cells(i, 1).Value))
            On Error GoTo 0

            ' Controlla se la data è uguale a dataGiorno23
            If data = dataGiorno23 Then
                almenoUnaCorrispondenza = True
                ' Verifica se riga destinazione non è 21 o 23
                If rigaDestinazione <> 21 And rigaDestinazione <> 23 Then
                    ' Copia i valori
                    wsDestinazione.Cells(rigaDestinazione, 1).Value = wsOrigine.Cells(i, 2).Value
                    wsDestinazione.Cells(rigaDestinazione, 4).Value = wsOrigine.Cells(i, 5).Value
                    wsDestinazione.Cells(rigaDestinazione, 5).Value = wsOrigine.Cells(i, 6).Value
                End If

                ' Aggiungi valori a A24 e U24, gestendo errori di conversione
                valoreC = Trim(wsOrigine.Cells(i, 3).Value)
                If Not IsEmpty(valoreC) Then
                    If Not ValoreEsistente(valoriC, valoreC) Then
                        valoriC.Add valoreC
                        concatenatoA24 = concatenatoA24 & IIf(concatenatoA24 = "", "", vbCrLf) & valoreC
                    End If
                End If

                valoreD = Trim(wsOrigine.Cells(i, 4).Value)
                If Not IsEmpty(valoreD) Then
                    If Not ValoreEsistente(valoriD, valoreD) Then
                        valoriD.Add valoreD
                        concatenatoU24 = concatenatoU24 & IIf(concatenatoU24 = "", "", vbCrLf) & valoreD
                    End If
                End If

                rigaDestinazione = rigaDestinazione + 1
            End If
        Next i

        ' Assegna le concatenazioni alle celle A24 e U24
        wsDestinazione.Range("A24").Value = concatenatoA24
        wsDestinazione.Range("U24").Value = concatenatoU24
    Else
        MsgBox "La cella K24 del foglio 'Elabora Giornaliera' non contiene una data valida.", vbExclamation
    End If

    Application.CutCopyMode = False
    Set valoriC = Nothing
    Set valoriD = Nothing
    Set wsOrigine = Nothing
    Set wsDestinazione = Nothing

End Sub

Function ValoreEsistente(valori As Collection, valore As String) As Boolean
    Dim v As Variant
    On Error Resume Next
    For Each v In valori
        If v = valore Then
            ValoreEsistente = True
            Exit Function
        End If
    Next v
    ValoreEsistente = False
End Function


```

## Componente: Modulo32.bas
Stream: VBA/Modulo32

```vba
Attribute VB_Name = "Modulo32"
Sub SmistaDatiGiorno24()
    Dim wsOrigine As Worksheet, wsDestinazione As Worksheet
    Dim ultimaRiga As Long, i As Long
    Dim data As Date, dataGiorno24 As Date
    Dim rigaDestinazione As Long
    Dim concatenatoA24 As String
    Dim concatenatoU24 As String
    Dim valoreC As String
    Dim valoreD As String
    Dim valoriC As Collection
    Dim valoriD As Collection
    Dim almenoUnaCorrispondenza As Boolean

    ' Imposta i fogli
    Set wsOrigine = ThisWorkbook.Sheets("Elabora Giornaliera")
    Set wsDestinazione = ThisWorkbook.Sheets("24")

    ' Trova l'ultima riga con dati nel foglio di origine
    ultimaRiga = wsOrigine.Cells(Rows.Count, 1).End(xlUp).Row

    ' Inizializza la riga di partenza per le colonne
    rigaDestinazione = 11

    ' Inizializza le celle di destinazione A24 e U24
    concatenatoA24 = ""
    concatenatoU24 = ""

    ' Inizializza le collezioni per rimuovere duplicati
    Set valoriC = New Collection
    Set valoriD = New Collection

    almenoUnaCorrispondenza = False

    'Gestisci potenziale errore in K25
    On Error Resume Next
    dataGiorno24 = DateValue(Worksheets("Elabora Giornaliera").Range("K25").Value)
    On Error GoTo 0

    'Controlla se la conversione della data è fallita
    If IsDate(dataGiorno24) Then
        ' Ciclo attraverso le righe del foglio di origine
        For i = 1 To ultimaRiga
            ' Controlla se la riga è vuota
            If IsEmpty(wsOrigine.Cells(i, 1).Value) Then Exit For

            On Error Resume Next
            data = CDate(Trim(wsOrigine.Cells(i, 1).Value))
            On Error GoTo 0

            ' Controlla se la data è uguale a dataGiorno24
            If data = dataGiorno24 Then
                almenoUnaCorrispondenza = True
                ' Verifica se riga destinazione non è 21 o 23
                If rigaDestinazione <> 21 And rigaDestinazione <> 23 Then
                    ' Copia i valori
                    wsDestinazione.Cells(rigaDestinazione, 1).Value = wsOrigine.Cells(i, 2).Value
                    wsDestinazione.Cells(rigaDestinazione, 4).Value = wsOrigine.Cells(i, 5).Value
                    wsDestinazione.Cells(rigaDestinazione, 5).Value = wsOrigine.Cells(i, 6).Value
                End If

                ' Aggiungi valori a A24 e U24, gestendo errori di conversione
                valoreC = Trim(wsOrigine.Cells(i, 3).Value)
                If Not IsEmpty(valoreC) Then
                    If Not ValoreEsistente(valoriC, valoreC) Then
                        valoriC.Add valoreC
                        concatenatoA24 = concatenatoA24 & IIf(concatenatoA24 = "", "", vbCrLf) & valoreC
                    End If
                End If

                valoreD = Trim(wsOrigine.Cells(i, 4).Value)
                If Not IsEmpty(valoreD) Then
                    If Not ValoreEsistente(valoriD, valoreD) Then
                        valoriD.Add valoreD
                        concatenatoU24 = concatenatoU24 & IIf(concatenatoU24 = "", "", vbCrLf) & valoreD
                    End If
                End If

                rigaDestinazione = rigaDestinazione + 1
            End If
        Next i

        ' Assegna le concatenazioni alle celle A24 e U24
        wsDestinazione.Range("A24").Value = concatenatoA24
        wsDestinazione.Range("U24").Value = concatenatoU24
    Else
        MsgBox "La cella K25 del foglio 'Elabora Giornaliera' non contiene una data valida.", vbExclamation
    End If

    Application.CutCopyMode = False
    Set valoriC = Nothing
    Set valoriD = Nothing
    Set wsOrigine = Nothing
    Set wsDestinazione = Nothing

End Sub

Function ValoreEsistente(valori As Collection, valore As String) As Boolean
    Dim v As Variant
    On Error Resume Next
    For Each v In valori
        If v = valore Then
            ValoreEsistente = True
            Exit Function
        End If
    Next v
    ValoreEsistente = False
End Function


```

## Componente: Modulo33.bas
Stream: VBA/Modulo33

```vba
Attribute VB_Name = "Modulo33"
Sub SmistaDatiGiorno25()
    Dim wsOrigine As Worksheet, wsDestinazione As Worksheet
    Dim ultimaRiga As Long, i As Long
    Dim data As Date, dataGiorno25 As Date
    Dim rigaDestinazione As Long
    Dim concatenatoA24 As String
    Dim concatenatoU24 As String
    Dim valoreC As String
    Dim valoreD As String
    Dim valoriC As Collection
    Dim valoriD As Collection
    Dim almenoUnaCorrispondenza As Boolean

    ' Imposta i fogli
    Set wsOrigine = ThisWorkbook.Sheets("Elabora Giornaliera")
    Set wsDestinazione = ThisWorkbook.Sheets("25")

    ' Trova l'ultima riga con dati nel foglio di origine
    ultimaRiga = wsOrigine.Cells(Rows.Count, 1).End(xlUp).Row

    ' Inizializza la riga di partenza per le colonne
    rigaDestinazione = 11

    ' Inizializza le celle di destinazione A24 e U24
    concatenatoA24 = ""
    concatenatoU24 = ""

    ' Inizializza le collezioni per rimuovere duplicati
    Set valoriC = New Collection
    Set valoriD = New Collection

    almenoUnaCorrispondenza = False

    'Gestisci potenziale errore in K26
    On Error Resume Next
    dataGiorno25 = DateValue(Worksheets("Elabora Giornaliera").Range("K26").Value)
    On Error GoTo 0

    'Controlla se la conversione della data è fallita
    If IsDate(dataGiorno25) Then
        ' Ciclo attraverso le righe del foglio di origine
        For i = 1 To ultimaRiga
            ' Controlla se la riga è vuota
            If IsEmpty(wsOrigine.Cells(i, 1).Value) Then Exit For

            On Error Resume Next
            data = CDate(Trim(wsOrigine.Cells(i, 1).Value))
            On Error GoTo 0

            ' Controlla se la data è uguale a dataGiorno25
            If data = dataGiorno25 Then
                almenoUnaCorrispondenza = True
                ' Verifica se riga destinazione non è 21 o 23
                If rigaDestinazione <> 21 And rigaDestinazione <> 23 Then
                    ' Copia i valori
                    wsDestinazione.Cells(rigaDestinazione, 1).Value = wsOrigine.Cells(i, 2).Value
                    wsDestinazione.Cells(rigaDestinazione, 4).Value = wsOrigine.Cells(i, 5).Value
                    wsDestinazione.Cells(rigaDestinazione, 5).Value = wsOrigine.Cells(i, 6).Value
                End If

                ' Aggiungi valori a A24 e U24, gestendo errori di conversione
                valoreC = Trim(wsOrigine.Cells(i, 3).Value)
                If Not IsEmpty(valoreC) Then
                    If Not ValoreEsistente(valoriC, valoreC) Then
                        valoriC.Add valoreC
                        concatenatoA24 = concatenatoA24 & IIf(concatenatoA24 = "", "", vbCrLf) & valoreC
                    End If
                End If

                valoreD = Trim(wsOrigine.Cells(i, 4).Value)
                If Not IsEmpty(valoreD) Then
                    If Not ValoreEsistente(valoriD, valoreD) Then
                        valoriD.Add valoreD
                        concatenatoU24 = concatenatoU24 & IIf(concatenatoU24 = "", "", vbCrLf) & valoreD
                    End If
                End If

                rigaDestinazione = rigaDestinazione + 1
            End If
        Next i

        ' Assegna le concatenazioni alle celle A24 e U24
        wsDestinazione.Range("A24").Value = concatenatoA24
        wsDestinazione.Range("U24").Value = concatenatoU24
    Else
        MsgBox "La cella K26 del foglio 'Elabora Giornaliera' non contiene una data valida.", vbExclamation
    End If

    Application.CutCopyMode = False
    Set valoriC = Nothing
    Set valoriD = Nothing
    Set wsOrigine = Nothing
    Set wsDestinazione = Nothing

End Sub

Function ValoreEsistente(valori As Collection, valore As String) As Boolean
    Dim v As Variant
    On Error Resume Next
    For Each v In valori
        If v = valore Then
            ValoreEsistente = True
            Exit Function
        End If
    Next v
    ValoreEsistente = False
End Function


```

## Componente: Modulo34.bas
Stream: VBA/Modulo34

```vba
Attribute VB_Name = "Modulo34"
Sub SmistaDatiGiorno26()
    Dim wsOrigine As Worksheet, wsDestinazione As Worksheet
    Dim ultimaRiga As Long, i As Long
    Dim data As Date, dataGiorno26 As Date
    Dim rigaDestinazione As Long
    Dim concatenatoA24 As String
    Dim concatenatoU24 As String
    Dim valoreC As String
    Dim valoreD As String
    Dim valoriC As Collection
    Dim valoriD As Collection
    Dim almenoUnaCorrispondenza As Boolean

    ' Imposta i fogli
    Set wsOrigine = ThisWorkbook.Sheets("Elabora Giornaliera")
    Set wsDestinazione = ThisWorkbook.Sheets("26")

    ' Trova l'ultima riga con dati nel foglio di origine
    ultimaRiga = wsOrigine.Cells(Rows.Count, 1).End(xlUp).Row

    ' Inizializza la riga di partenza per le colonne
    rigaDestinazione = 11

    ' Inizializza le celle di destinazione A24 e U24
    concatenatoA24 = ""
    concatenatoU24 = ""

    ' Inizializza le collezioni per rimuovere duplicati
    Set valoriC = New Collection
    Set valoriD = New Collection

    almenoUnaCorrispondenza = False

    'Gestisci potenziale errore in K27
    On Error Resume Next
    dataGiorno26 = DateValue(Worksheets("Elabora Giornaliera").Range("K27").Value)
    On Error GoTo 0

    'Controlla se la conversione della data è fallita
    If IsDate(dataGiorno26) Then
        ' Ciclo attraverso le righe del foglio di origine
        For i = 1 To ultimaRiga
            ' Controlla se la riga è vuota
            If IsEmpty(wsOrigine.Cells(i, 1).Value) Then Exit For

            On Error Resume Next
            data = CDate(Trim(wsOrigine.Cells(i, 1).Value))
            On Error GoTo 0

            ' Controlla se la data è uguale a dataGiorno26
            If data = dataGiorno26 Then
                almenoUnaCorrispondenza = True
                ' Verifica se riga destinazione non è 21 o 23
                If rigaDestinazione <> 21 And rigaDestinazione <> 23 Then
                    ' Copia i valori
                    wsDestinazione.Cells(rigaDestinazione, 1).Value = wsOrigine.Cells(i, 2).Value
                    wsDestinazione.Cells(rigaDestinazione, 4).Value = wsOrigine.Cells(i, 5).Value
                    wsDestinazione.Cells(rigaDestinazione, 5).Value = wsOrigine.Cells(i, 6).Value
                End If

                ' Aggiungi valori a A24 e U24, gestendo errori di conversione
                valoreC = Trim(wsOrigine.Cells(i, 3).Value)
                If Not IsEmpty(valoreC) Then
                    If Not ValoreEsistente(valoriC, valoreC) Then
                        valoriC.Add valoreC
                        concatenatoA24 = concatenatoA24 & IIf(concatenatoA24 = "", "", vbCrLf) & valoreC
                    End If
                End If

                valoreD = Trim(wsOrigine.Cells(i, 4).Value)
                If Not IsEmpty(valoreD) Then
                    If Not ValoreEsistente(valoriD, valoreD) Then
                        valoriD.Add valoreD
                        concatenatoU24 = concatenatoU24 & IIf(concatenatoU24 = "", "", vbCrLf) & valoreD
                    End If
                End If

                rigaDestinazione = rigaDestinazione + 1
            End If
        Next i

        ' Assegna le concatenazioni alle celle A24 e U24
        wsDestinazione.Range("A24").Value = concatenatoA24
        wsDestinazione.Range("U24").Value = concatenatoU24
    Else
        MsgBox "La cella K27 del foglio 'Elabora Giornaliera' non contiene una data valida.", vbExclamation
    End If

    Application.CutCopyMode = False
    Set valoriC = Nothing
    Set valoriD = Nothing
    Set wsOrigine = Nothing
    Set wsDestinazione = Nothing

End Sub

Function ValoreEsistente(valori As Collection, valore As String) As Boolean
    Dim v As Variant
    On Error Resume Next
    For Each v In valori
        If v = valore Then
            ValoreEsistente = True
            Exit Function
        End If
    Next v
    ValoreEsistente = False
End Function


```

## Componente: Modulo35.bas
Stream: VBA/Modulo35

```vba
Attribute VB_Name = "Modulo35"
Sub SmistaDatiGiorno27()
    Dim wsOrigine As Worksheet, wsDestinazione As Worksheet
    Dim ultimaRiga As Long, i As Long
    Dim data As Date, dataGiorno27 As Date
    Dim rigaDestinazione As Long
    Dim concatenatoA24 As String
    Dim concatenatoU24 As String
    Dim valoreC As String
    Dim valoreD As String
    Dim valoriC As Collection
    Dim valoriD As Collection
    Dim almenoUnaCorrispondenza As Boolean

    ' Imposta i fogli
    Set wsOrigine = ThisWorkbook.Sheets("Elabora Giornaliera")
    Set wsDestinazione = ThisWorkbook.Sheets("27")

    ' Trova l'ultima riga con dati nel foglio di origine
    ultimaRiga = wsOrigine.Cells(Rows.Count, 1).End(xlUp).Row

    ' Inizializza la riga di partenza per le colonne
    rigaDestinazione = 11

    ' Inizializza le celle di destinazione A24 e U24
    concatenatoA24 = ""
    concatenatoU24 = ""

    ' Inizializza le collezioni per rimuovere duplicati
    Set valoriC = New Collection
    Set valoriD = New Collection

    almenoUnaCorrispondenza = False

    'Gestisci potenziale errore in K28
    On Error Resume Next
    dataGiorno27 = DateValue(Worksheets("Elabora Giornaliera").Range("K28").Value)
    On Error GoTo 0

    'Controlla se la conversione della data è fallita
    If IsDate(dataGiorno27) Then
        ' Ciclo attraverso le righe del foglio di origine
        For i = 1 To ultimaRiga
            ' Controlla se la riga è vuota
            If IsEmpty(wsOrigine.Cells(i, 1).Value) Then Exit For

            On Error Resume Next
            data = CDate(Trim(wsOrigine.Cells(i, 1).Value))
            On Error GoTo 0

            ' Controlla se la data è uguale a dataGiorno27
            If data = dataGiorno27 Then
                almenoUnaCorrispondenza = True
                ' Verifica se riga destinazione non è 21 o 23
                If rigaDestinazione <> 21 And rigaDestinazione <> 23 Then
                    ' Copia i valori
                    wsDestinazione.Cells(rigaDestinazione, 1).Value = wsOrigine.Cells(i, 2).Value
                    wsDestinazione.Cells(rigaDestinazione, 4).Value = wsOrigine.Cells(i, 5).Value
                    wsDestinazione.Cells(rigaDestinazione, 5).Value = wsOrigine.Cells(i, 6).Value
                End If

                ' Aggiungi valori a A24 e U24, gestendo errori di conversione
                valoreC = Trim(wsOrigine.Cells(i, 3).Value)
                If Not IsEmpty(valoreC) Then
                    If Not ValoreEsistente(valoriC, valoreC) Then
                        valoriC.Add valoreC
                        concatenatoA24 = concatenatoA24 & IIf(concatenatoA24 = "", "", vbCrLf) & valoreC
                    End If
                End If

                valoreD = Trim(wsOrigine.Cells(i, 4).Value)
                If Not IsEmpty(valoreD) Then
                    If Not ValoreEsistente(valoriD, valoreD) Then
                        valoriD.Add valoreD
                        concatenatoU24 = concatenatoU24 & IIf(concatenatoU24 = "", "", vbCrLf) & valoreD
                    End If
                End If

                rigaDestinazione = rigaDestinazione + 1
            End If
        Next i

        ' Assegna le concatenazioni alle celle A24 e U24
        wsDestinazione.Range("A24").Value = concatenatoA24
        wsDestinazione.Range("U24").Value = concatenatoU24
    Else
        MsgBox "La cella K28 del foglio 'Elabora Giornaliera' non contiene una data valida.", vbExclamation
    End If

    Application.CutCopyMode = False
    Set valoriC = Nothing
    Set valoriD = Nothing
    Set wsOrigine = Nothing
    Set wsDestinazione = Nothing

End Sub

Function ValoreEsistente(valori As Collection, valore As String) As Boolean
    Dim v As Variant
    On Error Resume Next
    For Each v In valori
        If v = valore Then
            ValoreEsistente = True
            Exit Function
        End If
    Next v
    ValoreEsistente = False
End Function


```

## Componente: Modulo36.bas
Stream: VBA/Modulo36

```vba
Attribute VB_Name = "Modulo36"
Sub SmistaDatiGiorno28()
    Dim wsOrigine As Worksheet, wsDestinazione As Worksheet
    Dim ultimaRiga As Long, i As Long
    Dim data As Date, dataGiorno28 As Date
    Dim rigaDestinazione As Long
    Dim concatenatoA24 As String
    Dim concatenatoU24 As String
    Dim valoreC As String
    Dim valoreD As String
    Dim valoriC As Collection
    Dim valoriD As Collection
    Dim almenoUnaCorrispondenza As Boolean

    ' Imposta i fogli
    Set wsOrigine = ThisWorkbook.Sheets("Elabora Giornaliera")
    Set wsDestinazione = ThisWorkbook.Sheets("28")

    ' Trova l'ultima riga con dati nel foglio di origine
    ultimaRiga = wsOrigine.Cells(Rows.Count, 1).End(xlUp).Row

    ' Inizializza la riga di partenza per le colonne
    rigaDestinazione = 11

    ' Inizializza le celle di destinazione A24 e U24
    concatenatoA24 = ""
    concatenatoU24 = ""

    ' Inizializza le collezioni per rimuovere duplicati
    Set valoriC = New Collection
    Set valoriD = New Collection

    almenoUnaCorrispondenza = False

    'Gestisci potenziale errore in K29
    On Error Resume Next
    dataGiorno28 = DateValue(Worksheets("Elabora Giornaliera").Range("K29").Value)
    On Error GoTo 0

    'Controlla se la conversione della data è fallita
    If IsDate(dataGiorno28) Then
        ' Ciclo attraverso le righe del foglio di origine
        For i = 1 To ultimaRiga
            ' Controlla se la riga è vuota
            If IsEmpty(wsOrigine.Cells(i, 1).Value) Then Exit For

            On Error Resume Next
            data = CDate(Trim(wsOrigine.Cells(i, 1).Value))
            On Error GoTo 0

            ' Controlla se la data è uguale a dataGiorno28
            If data = dataGiorno28 Then
                almenoUnaCorrispondenza = True
                ' Verifica se riga destinazione non è 21 o 23
                If rigaDestinazione <> 21 And rigaDestinazione <> 23 Then
                    ' Copia i valori
                    wsDestinazione.Cells(rigaDestinazione, 1).Value = wsOrigine.Cells(i, 2).Value
                    wsDestinazione.Cells(rigaDestinazione, 4).Value = wsOrigine.Cells(i, 5).Value
                    wsDestinazione.Cells(rigaDestinazione, 5).Value = wsOrigine.Cells(i, 6).Value
                End If

                ' Aggiungi valori a A24 e U24, gestendo errori di conversione
                valoreC = Trim(wsOrigine.Cells(i, 3).Value)
                If Not IsEmpty(valoreC) Then
                    If Not ValoreEsistente(valoriC, valoreC) Then
                        valoriC.Add valoreC
                        concatenatoA24 = concatenatoA24 & IIf(concatenatoA24 = "", "", vbCrLf) & valoreC
                    End If
                End If

                valoreD = Trim(wsOrigine.Cells(i, 4).Value)
                If Not IsEmpty(valoreD) Then
                    If Not ValoreEsistente(valoriD, valoreD) Then
                        valoriD.Add valoreD
                        concatenatoU24 = concatenatoU24 & IIf(concatenatoU24 = "", "", vbCrLf) & valoreD
                    End If
                End If

                rigaDestinazione = rigaDestinazione + 1
            End If
        Next i

        ' Assegna le concatenazioni alle celle A24 e U24
        wsDestinazione.Range("A24").Value = concatenatoA24
        wsDestinazione.Range("U24").Value = concatenatoU24
    Else
        MsgBox "La cella K29 del foglio 'Elabora Giornaliera' non contiene una data valida.", vbExclamation
    End If

    Application.CutCopyMode = False
    Set valoriC = Nothing
    Set valoriD = Nothing
    Set wsOrigine = Nothing
    Set wsDestinazione = Nothing

End Sub

Function ValoreEsistente(valori As Collection, valore As String) As Boolean
    Dim v As Variant
    On Error Resume Next
    For Each v In valori
        If v = valore Then
            ValoreEsistente = True
            Exit Function
        End If
    Next v
    ValoreEsistente = False
End Function


```

## Componente: Modulo37.bas
Stream: VBA/Modulo37

```vba
Attribute VB_Name = "Modulo37"
Sub SmistaDatiGiorno29()
    Dim wsOrigine As Worksheet, wsDestinazione As Worksheet
    Dim ultimaRiga As Long, i As Long
    Dim data As Date, dataGiorno29 As Date
    Dim rigaDestinazione As Long
    Dim concatenatoA24 As String
    Dim concatenatoU24 As String
    Dim valoreC As String
    Dim valoreD As String
    Dim valoriC As Collection
    Dim valoriD As Collection
    Dim almenoUnaCorrispondenza As Boolean

    ' Imposta i fogli
    Set wsOrigine = ThisWorkbook.Sheets("Elabora Giornaliera")
    Set wsDestinazione = ThisWorkbook.Sheets("29")

    ' Trova l'ultima riga con dati nel foglio di origine
    ultimaRiga = wsOrigine.Cells(Rows.Count, 1).End(xlUp).Row

    ' Inizializza la riga di partenza per le colonne
    rigaDestinazione = 11

    ' Inizializza le celle di destinazione A24 e U24
    concatenatoA24 = ""
    concatenatoU24 = ""

    ' Inizializza le collezioni per rimuovere duplicati
    Set valoriC = New Collection
    Set valoriD = New Collection

    almenoUnaCorrispondenza = False

    'Gestisci potenziale errore in K30
    On Error Resume Next
    dataGiorno29 = DateValue(Worksheets("Elabora Giornaliera").Range("K30").Value)
    On Error GoTo 0

    'Controlla se la conversione della data è fallita
    If IsDate(dataGiorno29) Then
        ' Ciclo attraverso le righe del foglio di origine
        For i = 1 To ultimaRiga
            ' Controlla se la riga è vuota
            If IsEmpty(wsOrigine.Cells(i, 1).Value) Then Exit For

            On Error Resume Next
            data = CDate(Trim(wsOrigine.Cells(i, 1).Value))
            On Error GoTo 0

            ' Controlla se la data è uguale a dataGiorno29
            If data = dataGiorno29 Then
                almenoUnaCorrispondenza = True
                ' Verifica se riga destinazione non è 21 o 23
                If rigaDestinazione <> 21 And rigaDestinazione <> 23 Then
                    ' Copia i valori
                    wsDestinazione.Cells(rigaDestinazione, 1).Value = wsOrigine.Cells(i, 2).Value
                    wsDestinazione.Cells(rigaDestinazione, 4).Value = wsOrigine.Cells(i, 5).Value
                    wsDestinazione.Cells(rigaDestinazione, 5).Value = wsOrigine.Cells(i, 6).Value
                End If

                ' Aggiungi valori a A24 e U24, gestendo errori di conversione
                valoreC = Trim(wsOrigine.Cells(i, 3).Value)
                If Not IsEmpty(valoreC) Then
                    If Not ValoreEsistente(valoriC, valoreC) Then
                        valoriC.Add valoreC
                        concatenatoA24 = concatenatoA24 & IIf(concatenatoA24 = "", "", vbCrLf) & valoreC
                    End If
                End If

                valoreD = Trim(wsOrigine.Cells(i, 4).Value)
                If Not IsEmpty(valoreD) Then
                    If Not ValoreEsistente(valoriD, valoreD) Then
                        valoriD.Add valoreD
                        concatenatoU24 = concatenatoU24 & IIf(concatenatoU24 = "", "", vbCrLf) & valoreD
                    End If
                End If

                rigaDestinazione = rigaDestinazione + 1
            End If
        Next i

        ' Assegna le concatenazioni alle celle A24 e U24
        wsDestinazione.Range("A24").Value = concatenatoA24
        wsDestinazione.Range("U24").Value = concatenatoU24
    Else
        MsgBox "La cella K30 del foglio 'Elabora Giornaliera' non contiene una data valida.", vbExclamation
    End If

    Application.CutCopyMode = False
    Set valoriC = Nothing
    Set valoriD = Nothing
    Set wsOrigine = Nothing
    Set wsDestinazione = Nothing

End Sub

Function ValoreEsistente(valori As Collection, valore As String) As Boolean
    Dim v As Variant
    On Error Resume Next
    For Each v In valori
        If v = valore Then
            ValoreEsistente = True
            Exit Function
        End If
    Next v
    ValoreEsistente = False
End Function


```

## Componente: Modulo38.bas
Stream: VBA/Modulo38

```vba
Attribute VB_Name = "Modulo38"
Sub SmistaDatiGiorno30()
    Dim wsOrigine As Worksheet, wsDestinazione As Worksheet
    Dim ultimaRiga As Long, i As Long
    Dim data As Date, dataGiorno30 As Date
    Dim rigaDestinazione As Long
    Dim concatenatoA24 As String
    Dim concatenatoU24 As String
    Dim valoreC As String
    Dim valoreD As String
    Dim valoriC As Collection
    Dim valoriD As Collection
    Dim almenoUnaCorrispondenza As Boolean

    ' Imposta i fogli
    Set wsOrigine = ThisWorkbook.Sheets("Elabora Giornaliera")
    Set wsDestinazione = ThisWorkbook.Sheets("30")

    ' Trova l'ultima riga con dati nel foglio di origine
    ultimaRiga = wsOrigine.Cells(Rows.Count, 1).End(xlUp).Row

    ' Inizializza la riga di partenza per le colonne
    rigaDestinazione = 11

    ' Inizializza le celle di destinazione A24 e U24
    concatenatoA24 = ""
    concatenatoU24 = ""

    ' Inizializza le collezioni per rimuovere duplicati
    Set valoriC = New Collection
    Set valoriD = New Collection

    almenoUnaCorrispondenza = False

    'Gestisci potenziale errore in K31
    On Error Resume Next
    dataGiorno30 = DateValue(Worksheets("Elabora Giornaliera").Range("K31").Value)
    On Error GoTo 0

    'Controlla se la conversione della data è fallita
    If IsDate(dataGiorno30) Then
        ' Ciclo attraverso le righe del foglio di origine
        For i = 1 To ultimaRiga
            ' Controlla se la riga è vuota
            If IsEmpty(wsOrigine.Cells(i, 1).Value) Then Exit For

            On Error Resume Next
            data = CDate(Trim(wsOrigine.Cells(i, 1).Value))
            On Error GoTo 0

            ' Controlla se la data è uguale a dataGiorno30
            If data = dataGiorno30 Then
                almenoUnaCorrispondenza = True
                ' Verifica se riga destinazione non è 21 o 23
                If rigaDestinazione <> 21 And rigaDestinazione <> 23 Then
                    ' Copia i valori
                    wsDestinazione.Cells(rigaDestinazione, 1).Value = wsOrigine.Cells(i, 2).Value
                    wsDestinazione.Cells(rigaDestinazione, 4).Value = wsOrigine.Cells(i, 5).Value
                    wsDestinazione.Cells(rigaDestinazione, 5).Value = wsOrigine.Cells(i, 6).Value
                End If

                ' Aggiungi valori a A24 e U24, gestendo errori di conversione
                valoreC = Trim(wsOrigine.Cells(i, 3).Value)
                If Not IsEmpty(valoreC) Then
                    If Not ValoreEsistente(valoriC, valoreC) Then
                        valoriC.Add valoreC
                        concatenatoA24 = concatenatoA24 & IIf(concatenatoA24 = "", "", vbCrLf) & valoreC
                    End If
                End If

                valoreD = Trim(wsOrigine.Cells(i, 4).Value)
                If Not IsEmpty(valoreD) Then
                    If Not ValoreEsistente(valoriD, valoreD) Then
                        valoriD.Add valoreD
                        concatenatoU24 = concatenatoU24 & IIf(concatenatoU24 = "", "", vbCrLf) & valoreD
                    End If
                End If

                rigaDestinazione = rigaDestinazione + 1
            End If
        Next i

        ' Assegna le concatenazioni alle celle A24 e U24
        wsDestinazione.Range("A24").Value = concatenatoA24
        wsDestinazione.Range("U24").Value = concatenatoU24
    Else
        MsgBox "La cella K31 del foglio 'Elabora Giornaliera' non contiene una data valida.", vbExclamation
    End If

    Application.CutCopyMode = False
    Set valoriC = Nothing
    Set valoriD = Nothing
    Set wsOrigine = Nothing
    Set wsDestinazione = Nothing

End Sub

Function ValoreEsistente(valori As Collection, valore As String) As Boolean
    Dim v As Variant
    On Error Resume Next
    For Each v In valori
        If v = valore Then
            ValoreEsistente = True
            Exit Function
        End If
    Next v
    ValoreEsistente = False
End Function


```

## Componente: Modulo39.bas
Stream: VBA/Modulo39

```vba
Attribute VB_Name = "Modulo39"
Sub SmistaDatiGiorno31()
    Dim wsOrigine As Worksheet, wsDestinazione As Worksheet
    Dim ultimaRiga As Long, i As Long
    Dim data As Date, dataGiorno31 As Date
    Dim rigaDestinazione As Long
    Dim concatenatoA24 As String
    Dim concatenatoU24 As String
    Dim valoreC As String
    Dim valoreD As String
    Dim valoriC As Collection
    Dim valoriD As Collection
    Dim almenoUnaCorrispondenza As Boolean

    ' Imposta i fogli
    Set wsOrigine = ThisWorkbook.Sheets("Elabora Giornaliera")
    Set wsDestinazione = ThisWorkbook.Sheets("31")

    ' Trova l'ultima riga con dati nel foglio di origine
    ultimaRiga = wsOrigine.Cells(Rows.Count, 1).End(xlUp).Row

    ' Inizializza la riga di partenza per le colonne
    rigaDestinazione = 11

    ' Inizializza le celle di destinazione A24 e U24
    concatenatoA24 = ""
    concatenatoU24 = ""

    ' Inizializza le collezioni per rimuovere duplicati
    Set valoriC = New Collection
    Set valoriD = New Collection

    almenoUnaCorrispondenza = False

    'Gestisci potenziale errore in K32
    On Error Resume Next
    dataGiorno31 = DateValue(Worksheets("Elabora Giornaliera").Range("K32").Value)
    On Error GoTo 0

    'Controlla se la conversione della data è fallita
    If IsDate(dataGiorno31) Then
        ' Ciclo attraverso le righe del foglio di origine
        For i = 1 To ultimaRiga
            ' Controlla se la riga è vuota
            If IsEmpty(wsOrigine.Cells(i, 1).Value) Then Exit For

            On Error Resume Next
            data = CDate(Trim(wsOrigine.Cells(i, 1).Value))
            On Error GoTo 0

            ' Controlla se la data è uguale a dataGiorno31
            If data = dataGiorno31 Then
                almenoUnaCorrispondenza = True
                ' Verifica se riga destinazione non è 21 o 23
                If rigaDestinazione <> 21 And rigaDestinazione <> 23 Then
                    ' Copia i valori
                    wsDestinazione.Cells(rigaDestinazione, 1).Value = wsOrigine.Cells(i, 2).Value
                    wsDestinazione.Cells(rigaDestinazione, 4).Value = wsOrigine.Cells(i, 5).Value
                    wsDestinazione.Cells(rigaDestinazione, 5).Value = wsOrigine.Cells(i, 6).Value
                End If

                ' Aggiungi valori a A24 e U24, gestendo errori di conversione
                valoreC = Trim(wsOrigine.Cells(i, 3).Value)
                If Not IsEmpty(valoreC) Then
                    If Not ValoreEsistente(valoriC, valoreC) Then
                        valoriC.Add valoreC
                        concatenatoA24 = concatenatoA24 & IIf(concatenatoA24 = "", "", vbCrLf) & valoreC
                    End If
                End If

                valoreD = Trim(wsOrigine.Cells(i, 4).Value)
                If Not IsEmpty(valoreD) Then
                    If Not ValoreEsistente(valoriD, valoreD) Then
                        valoriD.Add valoreD
                        concatenatoU24 = concatenatoU24 & IIf(concatenatoU24 = "", "", vbCrLf) & valoreD
                    End If
                End If

                rigaDestinazione = rigaDestinazione + 1
            End If
        Next i

        ' Assegna le concatenazioni alle celle A24 e U24
        wsDestinazione.Range("A24").Value = concatenatoA24
        wsDestinazione.Range("U24").Value = concatenatoU24
    Else
        MsgBox "La cella K32 del foglio 'Elabora Giornaliera' non contiene una data valida.", vbExclamation
    End If

    Application.CutCopyMode = False
    Set valoriC = Nothing
    Set valoriD = Nothing
    Set wsOrigine = Nothing
    Set wsDestinazione = Nothing

End Sub

Function ValoreEsistente(valori As Collection, valore As String) As Boolean
    Dim v As Variant
    On Error Resume Next
    For Each v In valori
        If v = valore Then
            ValoreEsistente = True
            Exit Function
        End If
    Next v
    ValoreEsistente = False
End Function


```

## Componente: Modulo40.bas
Stream: VBA/Modulo40

```vba
Attribute VB_Name = "Modulo40"
Sub EseguiTuttiSmista()

    Dim i As Integer

    ' Check the value of cell B4 on sheet "rif.VBA"
    If ThisWorkbook.Sheets("rif.VBA").Range("B4").Value <> "MISURA" Then

        ' Ciclo da 1 a 31 per chiamare tutte le subroutine
        For i = 1 To 31
            Application.Run "SmistaDatiGiorno" & i
        Next i
    Else
        MsgBox "Il consuntivo non è una misura. Non viene compilato il dettaglio ore."
    End If
Call CancellaERinominaFogliOre
  Call ElaboraConsuntivoSquadra
End Sub


```

## Componente: Modulo41.bas
Stream: VBA/Modulo41

```vba
Attribute VB_Name = "Modulo41"
Sub VerificaConsuntivo()

    Dim msgError As String
    Dim wsConsuntivo As Worksheet, wsRifVBA As Worksheet

    ' Variabili per ripristino impostazioni Applicazione
    Dim prevStatusBar As Variant
    Dim prevEnableEvents As Boolean
    Dim prevScreenUpdating As Boolean
    Dim erroreValidazionePresente As Boolean ' Flag per sapere se sono stati trovati errori di validazione
    Dim erroreVBAPresente As Boolean      ' Flag per sapere se si è verificato un errore VBA

    erroreValidazionePresente = False
    erroreVBAPresente = False

    ' Salva lo stato corrente delle impostazioni e le modifica
    prevStatusBar = Application.StatusBar
    prevEnableEvents = Application.EnableEvents
    prevScreenUpdating = Application.ScreenUpdating

    Application.EnableEvents = False
    Application.ScreenUpdating = False
    Application.StatusBar = "Verifica Consuntivo in corso..."

    On Error GoTo GestoreErroriImprevisti

    Set wsConsuntivo = ThisWorkbook.Sheets("Consuntivo")
    Set wsRifVBA = ThisWorkbook.Sheets("rif.VBA")

    ' Verifica cella C4 nel foglio rif.VBA
    If wsRifVBA.Range("C4").Value = "" Then msgError = msgError & "Inserire assistente TCL." & vbCrLf

    ' Verifica celle vuote nel foglio Consuntivo
    If Trim(wsConsuntivo.Range("A22").Value) = "" Then msgError = msgError & "Il consuntivo risulta vuoto." & vbCrLf
    If wsConsuntivo.Range("J10").Value = "" Then msgError = msgError & "Inserisci data." & vbCrLf
    If wsConsuntivo.Range("D14").Value = "" Then msgError = msgError & "Inserisci descrizione lavoro." & vbCrLf
    If wsConsuntivo.Range("J14").Value = "" Or InStr(1, CStr(wsConsuntivo.Range("J14").Value), "ERRORE", vbTextCompare) > 0 Then msgError = msgError & "Mancato rilevamento formato nome file o errore rilevato." & vbCrLf
    If wsConsuntivo.Range("B56").Value = "" Or wsConsuntivo.Range("K16").Value = "" Then msgError = msgError & "Inserisci Persona che compila il consuntivo o controlla la cella K16." & vbCrLf
    If wsConsuntivo.Range("H12").Value = "" Or wsConsuntivo.Range("H56").Value = "" Then msgError = msgError & "Inserisci Assistente TCL o controlla la cella H56." & vbCrLf

    ' Verifica uguaglianza ore spese, solo se B4 di rif.VBA è diverso da "MISURA"
    If UCase(Trim(CStr(wsRifVBA.Range("B4").Value))) <> "MISURA" Then
        On Error Resume Next
        Dim valP21 As Variant, valQ5 As Variant
        valP21 = wsConsuntivo.Range("P21").Value
        valQ5 = wsConsuntivo.Range("Q5").Value
        If IsNumeric(valP21) And IsNumeric(valQ5) Then
            If CDbl(valP21) <> CDbl(valQ5) Then
                msgError = msgError & "Quantità ore spese attività diversa tra Giornaliera e dettaglio ore (P21 vs Q5)." & vbCrLf
            End If
        Else
            If Not (IsError(valP21) Or IsError(valQ5)) Then
                 msgError = msgError & "Impossibile confrontare ore spese (P21 vs Q5) a causa di valori non numerici o vuoti." & vbCrLf
            End If
        End If
        Err.Clear
        On Error GoTo GestoreErroriImprevisti
    End If

    ' Verifica congruenza economica
    On Error Resume Next
    Dim valJ8 As Variant, valI45 As Variant
    valJ8 = wsConsuntivo.Range("J8").Value
    valI45 = wsConsuntivo.Range("I45").Value
    If IsNumeric(valJ8) And IsNumeric(valI45) Then
        If CDbl(valJ8) <> CDbl(valI45) Then
            msgError = msgError & "La somma economica nel Consuntivo non è congruente (J8 vs I45)." & vbCrLf
        End If
    Else
        If Not (IsError(valJ8) Or IsError(valI45)) Then
            msgError = msgError & "Impossibile confrontare somme economiche (J8 vs I45) a causa di valori non numerici o vuoti." & vbCrLf
        End If
    End If
    Err.Clear
    On Error GoTo GestoreErroriImprevisti

    'Gestione errori #RIF! o altri errori di cella
    If IsError(wsConsuntivo.Range("J10").Value) Then msgError = msgError & "La cella J10 (Data) contiene un errore." & vbCrLf
    If IsError(wsConsuntivo.Range("D14").Value) Then msgError = msgError & "La cella D14 (Descrizione Lavoro) contiene un errore." & vbCrLf
    If IsError(wsConsuntivo.Range("I45").Value) Then msgError = msgError & "La cella I45 (Totale Economico Dettaglio) contiene un errore." & vbCrLf
    If IsError(wsConsuntivo.Range("J14").Value) Then msgError = msgError & "La cella J14 (Nome File) contiene un errore." & vbCrLf
    If IsError(wsConsuntivo.Range("H12").Value) Then msgError = msgError & "La cella H12 (Assistente TCL Riepilogo) contiene un errore." & vbCrLf
    If IsError(wsConsuntivo.Range("P21").Value) Then msgError = msgError & "La cella P21 (Ore Spese Giornaliera) contiene un errore." & vbCrLf
    If IsError(wsConsuntivo.Range("Q5").Value) Then msgError = msgError & "La cella Q5 (Ore Spese Dettaglio) contiene un errore." & vbCrLf
    If IsError(wsConsuntivo.Range("J8").Value) Then msgError = msgError & "La cella J8 (Totale Economico Riepilogo) contiene un errore." & vbCrLf
    If IsError(wsConsuntivo.Range("K16").Value) Then msgError = msgError & "La cella K16 contiene un errore." & vbCrLf
    If IsError(wsConsuntivo.Range("H56").Value) Then msgError = msgError & "La cella H56 contiene un errore." & vbCrLf

    ' --- Funzione di adattamento automatico altezza righe RIMOSSA ---
    ' wsConsuntivo.Rows(13).AutoFit
    ' wsConsuntivo.Rows(14).AutoFit
    ' wsConsuntivo.Rows(15).AutoFit

    ' Messaggio finale
    If msgError = "" Then
        Application.StatusBar = "Verifica Consuntivo: Nessun problema rilevato."
        ' MsgBox "Nessun problema rilevato.", vbInformation, "Esito Verifica" ' RIMOSSO
        Application.Wait Now + TimeValue("00:00:02") ' Pausa per visualizzare il messaggio sulla barra di stato
    Else
        erroreValidazionePresente = True ' Segnala che sono stati trovati errori di validazione
        Application.StatusBar = "Verifica Consuntivo: Rilevati problemi! Vedere dettagli."
        MsgBox msgError, vbExclamation, "Problemi Rilevati nel Consuntivo" ' MANTENUTO
    End If

    GoTo RipristinaImpostazioni ' Salta il gestore errori se tutto è andato liscio

GestoreErroriImprevisti:
    erroreVBAPresente = True ' Segnala che si è verificato un errore VBA
    Application.StatusBar = "Verifica Consuntivo: Errore VBA n. " & Err.Number & " - " & Err.Description
    ' MsgBox per errore VBA imprevisto può essere mantenuto se si desidera una notifica più forte per questi
    ' Se anche questo deve essere silenzioso, commentare la riga MsgBox sottostante
    MsgBox "Si è verificato un errore imprevisto nella macro VerificaConsuntivo." & vbCrLf & _
           "Errore " & Err.Number & ": " & Err.Description, vbCritical, "Errore Macro"

RipristinaImpostazioni:
    Application.EnableEvents = prevEnableEvents
    Application.ScreenUpdating = prevScreenUpdating

    ' Logica per resettare la barra di stato
    If erroreVBAPresente Then
        ' Lascia il messaggio di errore VBA sulla barra di stato (l'utente è stato avvisato dal MsgBox)
    ElseIf erroreValidazionePresente Then
        ' L'utente ha visto il MsgBox dei problemi di validazione, possiamo resettare la barra
        Application.StatusBar = False
    Else ' Nessun errore VBA e nessun errore di validazione (msgError era vuoto)
        Application.StatusBar = False
    End If

    Set wsConsuntivo = Nothing ' Buona pratica rilasciare gli oggetti
    Set wsRifVBA = Nothing   ' Buona pratica rilasciare gli oggetti

End Sub




```

## Componente: Modulo42.bas
Stream: VBA/Modulo42

```vba
Attribute VB_Name = "Modulo42"
Sub ElaboraTUTTO()
  Call CaricaDatiMultiplo
  Call elaboraDati
  Call EseguiTuttiSmista
  Call ElaboraConsuntivoSquadra
  Call VerificaConsuntivo
  MsgBox "Tutti i moduli eseguiti correttamente.", vbInformation
End Sub


```

## Componente: Modulo43.bas
Stream: VBA/Modulo43

```vba
Attribute VB_Name = "Modulo43"
Sub EeseguiTUTTO()
Call ElaboraTUTTO
Call StampaFogli
End Sub

```

## Componente: Modulo14.bas
Stream: VBA/Modulo14

```vba
Attribute VB_Name = "Modulo14"
Sub SmistaDatiGiorno6()
    Dim wsOrigine As Worksheet, wsDestinazione As Worksheet
    Dim ultimaRiga As Long, i As Long
    Dim data As Date, dataGiorno6 As Date
    Dim rigaDestinazione As Long
    Dim concatenatoA24 As String
    Dim concatenatoU24 As String
    Dim valoreC As String
    Dim valoreD As String
    Dim valoriC As Collection
    Dim valoriD As Collection
    Dim almenoUnaCorrispondenza As Boolean

    ' Imposta i fogli
    Set wsOrigine = ThisWorkbook.Sheets("Elabora Giornaliera")
    Set wsDestinazione = ThisWorkbook.Sheets("6")

    ' Trova l'ultima riga con dati nel foglio di origine
    ultimaRiga = wsOrigine.Cells(Rows.Count, 1).End(xlUp).Row

    ' Inizializza la riga di partenza per le colonne
    rigaDestinazione = 11

    ' Inizializza le celle di destinazione A24 e U24
    concatenatoA24 = ""
    concatenatoU24 = ""

    ' Inizializza le collezioni per rimuovere duplicati
    Set valoriC = New Collection
    Set valoriD = New Collection

    almenoUnaCorrispondenza = False

    'Gestisci potenziale errore in K7
    On Error Resume Next
    dataGiorno6 = DateValue(Worksheets("Elabora Giornaliera").Range("K7").Value)
    On Error GoTo 0

    'Controlla se la conversione della data è fallita
    If IsDate(dataGiorno6) Then
        ' Ciclo attraverso le righe del foglio di origine
        For i = 1 To ultimaRiga
            ' Controlla se la riga è vuota
            If IsEmpty(wsOrigine.Cells(i, 1).Value) Then Exit For

            On Error Resume Next
            data = CDate(Trim(wsOrigine.Cells(i, 1).Value))
            On Error GoTo 0

            ' Controlla se la data è uguale a dataGiorno6
            If data = dataGiorno6 Then
                almenoUnaCorrispondenza = True
                ' Verifica se riga destinazione non è 21 o 23
                If rigaDestinazione <> 21 And rigaDestinazione <> 23 Then
                    ' Copia i valori
                    wsDestinazione.Cells(rigaDestinazione, 1).Value = wsOrigine.Cells(i, 2).Value
                    wsDestinazione.Cells(rigaDestinazione, 4).Value = wsOrigine.Cells(i, 5).Value
                    wsDestinazione.Cells(rigaDestinazione, 5).Value = wsOrigine.Cells(i, 6).Value
                End If

                ' Aggiungi valori a A24 e U24, gestendo errori di conversione
                valoreC = Trim(wsOrigine.Cells(i, 3).Value)
                If Not IsEmpty(valoreC) Then
                    If Not ValoreEsistente(valoriC, valoreC) Then
                        valoriC.Add valoreC
                        concatenatoA24 = concatenatoA24 & IIf(concatenatoA24 = "", "", vbCrLf) & valoreC
                    End If
                End If

                valoreD = Trim(wsOrigine.Cells(i, 4).Value)
                If Not IsEmpty(valoreD) Then
                    If Not ValoreEsistente(valoriD, valoreD) Then
                        valoriD.Add valoreD
                        concatenatoU24 = concatenatoU24 & IIf(concatenatoU24 = "", "", vbCrLf) & valoreD
                    End If
                End If

                rigaDestinazione = rigaDestinazione + 1
            End If
        Next i

        ' Assegna le concatenazioni alle celle A24 e U24
        wsDestinazione.Range("A24").Value = concatenatoA24
        wsDestinazione.Range("U24").Value = concatenatoU24
    Else
        MsgBox "La cella K7 del foglio 'Elabora Giornaliera' non contiene una data valida.", vbExclamation
    End If

    Application.CutCopyMode = False
    Set valoriC = Nothing
    Set valoriD = Nothing
    Set wsOrigine = Nothing
    Set wsDestinazione = Nothing

End Sub

Function ValoreEsistente(valori As Collection, valore As String) As Boolean
    Dim v As Variant
    On Error Resume Next
    For Each v In valori
        If v = valore Then
            ValoreEsistente = True
            Exit Function
        End If
    Next v
    ValoreEsistente = False
End Function


```

## Componente: Modulo15.bas
Stream: VBA/Modulo15

```vba
Attribute VB_Name = "Modulo15"
Sub SmistaDatiGiorno7()
    Dim wsOrigine As Worksheet, wsDestinazione As Worksheet
    Dim ultimaRiga As Long, i As Long
    Dim data As Date, dataGiorno7 As Date
    Dim rigaDestinazione As Long
    Dim concatenatoA24 As String
    Dim concatenatoU24 As String
    Dim valoreC As String
    Dim valoreD As String
    Dim valoriC As Collection
    Dim valoriD As Collection
    Dim almenoUnaCorrispondenza As Boolean

    ' Imposta i fogli
    Set wsOrigine = ThisWorkbook.Sheets("Elabora Giornaliera")
    Set wsDestinazione = ThisWorkbook.Sheets("7")

    ' Trova l'ultima riga con dati nel foglio di origine
    ultimaRiga = wsOrigine.Cells(Rows.Count, 1).End(xlUp).Row

    ' Inizializza la riga di partenza per le colonne
    rigaDestinazione = 11

    ' Inizializza le celle di destinazione A24 e U24
    concatenatoA24 = ""
    concatenatoU24 = ""

    ' Inizializza le collezioni per rimuovere duplicati
    Set valoriC = New Collection
    Set valoriD = New Collection

    almenoUnaCorrispondenza = False

    'Gestisci potenziale errore in K8
    On Error Resume Next
    dataGiorno7 = DateValue(Worksheets("Elabora Giornaliera").Range("K8").Value)
    On Error GoTo 0

    'Controlla se la conversione della data è fallita
    If IsDate(dataGiorno7) Then
        ' Ciclo attraverso le righe del foglio di origine
        For i = 1 To ultimaRiga
            ' Controlla se la riga è vuota
            If IsEmpty(wsOrigine.Cells(i, 1).Value) Then Exit For

            On Error Resume Next
            data = CDate(Trim(wsOrigine.Cells(i, 1).Value))
            On Error GoTo 0

            ' Controlla se la data è uguale a dataGiorno7
            If data = dataGiorno7 Then
                almenoUnaCorrispondenza = True
                ' Verifica se riga destinazione non è 21 o 23
                If rigaDestinazione <> 21 And rigaDestinazione <> 23 Then
                    ' Copia i valori
                    wsDestinazione.Cells(rigaDestinazione, 1).Value = wsOrigine.Cells(i, 2).Value
                    wsDestinazione.Cells(rigaDestinazione, 4).Value = wsOrigine.Cells(i, 5).Value
                    wsDestinazione.Cells(rigaDestinazione, 5).Value = wsOrigine.Cells(i, 6).Value
                End If

                ' Aggiungi valori a A24 e U24, gestendo errori di conversione
                valoreC = Trim(wsOrigine.Cells(i, 3).Value)
                If Not IsEmpty(valoreC) Then
                    If Not ValoreEsistente(valoriC, valoreC) Then
                        valoriC.Add valoreC
                        concatenatoA24 = concatenatoA24 & IIf(concatenatoA24 = "", "", vbCrLf) & valoreC
                    End If
                End If

                valoreD = Trim(wsOrigine.Cells(i, 4).Value)
                If Not IsEmpty(valoreD) Then
                    If Not ValoreEsistente(valoriD, valoreD) Then
                        valoriD.Add valoreD
                        concatenatoU24 = concatenatoU24 & IIf(concatenatoU24 = "", "", vbCrLf) & valoreD
                    End If
                End If

                rigaDestinazione = rigaDestinazione + 1
            End If
        Next i

        ' Assegna le concatenazioni alle celle A24 e U24
        wsDestinazione.Range("A24").Value = concatenatoA24
        wsDestinazione.Range("U24").Value = concatenatoU24
    Else
        MsgBox "La cella K8 del foglio 'Elabora Giornaliera' non contiene una data valida.", vbExclamation
    End If

    Application.CutCopyMode = False
    Set valoriC = Nothing
    Set valoriD = Nothing
    Set wsOrigine = Nothing
    Set wsDestinazione = Nothing

End Sub

Function ValoreEsistente(valori As Collection, valore As String) As Boolean
    Dim v As Variant
    On Error Resume Next
    For Each v In valori
        If v = valore Then
            ValoreEsistente = True
            Exit Function
        End If
    Next v
    ValoreEsistente = False
End Function


```

## Componente: Modulo16.bas
Stream: VBA/Modulo16

```vba
Attribute VB_Name = "Modulo16"
Sub SmistaDatiGiorno8()
    Dim wsOrigine As Worksheet, wsDestinazione As Worksheet
    Dim ultimaRiga As Long, i As Long
    Dim data As Date, dataGiorno8 As Date
    Dim rigaDestinazione As Long
    Dim concatenatoA24 As String
    Dim concatenatoU24 As String
    Dim valoreC As String
    Dim valoreD As String
    Dim valoriC As Collection
    Dim valoriD As Collection
    Dim almenoUnaCorrispondenza As Boolean

    ' Imposta i fogli
    Set wsOrigine = ThisWorkbook.Sheets("Elabora Giornaliera")
    Set wsDestinazione = ThisWorkbook.Sheets("8")

    ' Trova l'ultima riga con dati nel foglio di origine
    ultimaRiga = wsOrigine.Cells(Rows.Count, 1).End(xlUp).Row

    ' Inizializza la riga di partenza per le colonne
    rigaDestinazione = 11

    ' Inizializza le celle di destinazione A24 e U24
    concatenatoA24 = ""
    concatenatoU24 = ""

    ' Inizializza le collezioni per rimuovere duplicati
    Set valoriC = New Collection
    Set valoriD = New Collection

    almenoUnaCorrispondenza = False

    'Gestisci potenziale errore in K9
    On Error Resume Next
    dataGiorno8 = DateValue(Worksheets("Elabora Giornaliera").Range("K9").Value)
    On Error GoTo 0

    'Controlla se la conversione della data è fallita
    If IsDate(dataGiorno8) Then
        ' Ciclo attraverso le righe del foglio di origine
        For i = 1 To ultimaRiga
            ' Controlla se la riga è vuota
            If IsEmpty(wsOrigine.Cells(i, 1).Value) Then Exit For

            On Error Resume Next
            data = CDate(Trim(wsOrigine.Cells(i, 1).Value))
            On Error GoTo 0

            ' Controlla se la data è uguale a dataGiorno8
            If data = dataGiorno8 Then
                almenoUnaCorrispondenza = True
                ' Verifica se riga destinazione non è 21 o 23
                If rigaDestinazione <> 21 And rigaDestinazione <> 23 Then
                    ' Copia i valori
                    wsDestinazione.Cells(rigaDestinazione, 1).Value = wsOrigine.Cells(i, 2).Value
                    wsDestinazione.Cells(rigaDestinazione, 4).Value = wsOrigine.Cells(i, 5).Value
                    wsDestinazione.Cells(rigaDestinazione, 5).Value = wsOrigine.Cells(i, 6).Value
                End If

                ' Aggiungi valori a A24 e U24, gestendo errori di conversione
                valoreC = Trim(wsOrigine.Cells(i, 3).Value)
                If Not IsEmpty(valoreC) Then
                    If Not ValoreEsistente(valoriC, valoreC) Then
                        valoriC.Add valoreC
                        concatenatoA24 = concatenatoA24 & IIf(concatenatoA24 = "", "", vbCrLf) & valoreC
                    End If
                End If

                valoreD = Trim(wsOrigine.Cells(i, 4).Value)
                If Not IsEmpty(valoreD) Then
                    If Not ValoreEsistente(valoriD, valoreD) Then
                        valoriD.Add valoreD
                        concatenatoU24 = concatenatoU24 & IIf(concatenatoU24 = "", "", vbCrLf) & valoreD
                    End If
                End If

                rigaDestinazione = rigaDestinazione + 1
            End If
        Next i

        ' Assegna le concatenazioni alle celle A24 e U24
        wsDestinazione.Range("A24").Value = concatenatoA24
        wsDestinazione.Range("U24").Value = concatenatoU24
    Else
        MsgBox "La cella K9 del foglio 'Elabora Giornaliera' non contiene una data valida.", vbExclamation
    End If

    Application.CutCopyMode = False
    Set valoriC = Nothing
    Set valoriD = Nothing
    Set wsOrigine = Nothing
    Set wsDestinazione = Nothing

End Sub

Function ValoreEsistente(valori As Collection, valore As String) As Boolean
    Dim v As Variant
    On Error Resume Next
    For Each v In valori
        If v = valore Then
            ValoreEsistente = True
            Exit Function
        End If
    Next v
    ValoreEsistente = False
End Function


```

## Componente: Modulo10.bas
Stream: VBA/Modulo10

```vba
Attribute VB_Name = "Modulo10"
Sub SmistaDatiGiorno1()
    Dim wsOrigine As Worksheet, wsDestinazione As Worksheet
    Dim ultimaRiga As Long, i As Long
    Dim data As Date, dataGiorno1 As Date
    Dim rigaDestinazione As Long
    Dim concatenatoA24 As String
    Dim concatenatoU24 As String
    Dim valoreC As String
    Dim valoreD As String
    Dim valoriC As Collection
    Dim valoriD As Collection
    Dim almenoUnaCorrispondenza As Boolean

    ' Imposta la data di riferimento per il giorno 1
    dataGiorno1 = DateValue(Worksheets("Elabora Giornaliera").Range("K2").Value) 'Data modificata per il giorno 1

    ' Imposta i fogli
    Set wsOrigine = ThisWorkbook.Sheets("Elabora Giornaliera")
    Set wsDestinazione = ThisWorkbook.Sheets("1")

    ' Trova l'ultima riga con dati nel foglio di origine
    ultimaRiga = wsOrigine.Cells(Rows.Count, "A").End(xlUp).Row

    ' Inizializza la riga di partenza per le colonne
    rigaDestinazione = 11

    ' Inizializza le celle di destinazione A24 e U24
    concatenatoA24 = ""
    concatenatoU24 = ""

    ' Inizializza le collezioni per rimuovere duplicati
    Set valoriC = New Collection
    Set valoriD = New Collection

    almenoUnaCorrispondenza = False
    ' Ciclo attraverso le righe del foglio di origine
    For i = 1 To ultimaRiga
        ' Controlla se la riga è vuota (verifica su colonna A)
        If IsEmpty(wsOrigine.Cells(i, "A").Value) Then Exit For ' Esce dal ciclo se trova una riga vuota

        On Error Resume Next
        data = CDate(Trim(wsOrigine.Cells(i, "A").Value))
        On Error GoTo 0

        ' Controlla se la data è uguale a "01/01/2025"
        If data = dataGiorno1 Then
            almenoUnaCorrispondenza = True

            ' Copia valori solo se rigaDestinazione <= 20
            If rigaDestinazione <= 20 Then
                wsDestinazione.Cells(rigaDestinazione, "A").Value = wsOrigine.Cells(i, "B").Value
                wsDestinazione.Cells(rigaDestinazione, "D").Value = wsOrigine.Cells(i, "E").Value
                wsDestinazione.Cells(rigaDestinazione, "E").Value = wsOrigine.Cells(i, "F").Value
                rigaDestinazione = rigaDestinazione + 1
            End If

            ' Aggiunge valori a A24 e U24 indipendentemente da rigaDestinazione
            valoreC = Trim(wsOrigine.Cells(i, "C").Value)
            If Not IsEmpty(valoreC) Then
                If Not ValoreEsistente(valoriC, valoreC) Then
                    valoriC.Add valoreC
                    concatenatoA24 = concatenatoA24 & IIf(concatenatoA24 = "", "", vbCrLf) & valoreC
                End If
            End If

            valoreD = Trim(wsOrigine.Cells(i, "D").Value)
            If Not IsEmpty(valoreD) Then
                If Not ValoreEsistente(valoriD, valoreD) Then
                    valoriD.Add valoreD
                    concatenatoU24 = concatenatoU24 & IIf(concatenatoU24 = "", "", vbCrLf) & valoreD
                End If
            End If

        End If
    Next i
    'Aggiorna A24 e U24 solo dopo aver elaborato tutte le righe
    If almenoUnaCorrispondenza Then
        wsDestinazione.Range("A24").Value = concatenatoA24
        wsDestinazione.Range("U24").Value = concatenatoU24
    End If

    Application.CutCopyMode = False
End Sub

Function ValoreEsistente(valori As Collection, valore As String) As Boolean
    Dim v As Variant
    On Error Resume Next
    For Each v In valori
        If v = valore Then
            ValoreEsistente = True
            Exit Function
        End If
    Next v
    ValoreEsistente = False
End Function


```

## Componente: Modulo11.bas
Stream: VBA/Modulo11

```vba
Attribute VB_Name = "Modulo11"
Sub SmistaDatiGiorno3()
    Dim wsOrigine As Worksheet, wsDestinazione As Worksheet
    Dim ultimaRiga As Long, i As Long
    Dim data As Date, dataGiorno3 As Date
    Dim rigaDestinazione As Long
    Dim concatenatoA24 As String
    Dim concatenatoU24 As String
    Dim valoreC As String
    Dim valoreD As String
    Dim valoriC As Collection
    Dim valoriD As Collection
    Dim almenoUnaCorrispondenza As Boolean

    ' Imposta i fogli
    Set wsOrigine = ThisWorkbook.Sheets("Elabora Giornaliera")
    Set wsDestinazione = ThisWorkbook.Sheets("3")

    ' Trova l'ultima riga con dati nel foglio di origine
    ultimaRiga = wsOrigine.Cells(Rows.Count, 1).End(xlUp).Row

    ' Inizializza la riga di partenza per le colonne
    rigaDestinazione = 11

    ' Inizializza le celle di destinazione A24 e U24
    concatenatoA24 = ""
    concatenatoU24 = ""

    ' Inizializza le collezioni per rimuovere duplicati
    Set valoriC = New Collection
    Set valoriD = New Collection

    almenoUnaCorrispondenza = False

    'Gestisci potenziale errore in K4
    On Error Resume Next
    dataGiorno3 = DateValue(Worksheets("Elabora Giornaliera").Range("K4").Value)
    On Error GoTo 0

    'Controlla se la conversione della data è fallita
    If IsDate(dataGiorno3) Then
        ' Ciclo attraverso le righe del foglio di origine
        For i = 1 To ultimaRiga
            ' Controlla se la riga è vuota
            If IsEmpty(wsOrigine.Cells(i, 1).Value) Then Exit For 'Esce solo dal ciclo For

            On Error Resume Next
            data = CDate(Trim(wsOrigine.Cells(i, 1).Value))
            On Error GoTo 0

            ' Controlla se la data è uguale a dataGiorno3
            If data = dataGiorno3 Then
                almenoUnaCorrispondenza = True
                ' Verifica se riga destinazione non è 21 o 23
                If rigaDestinazione <> 21 And rigaDestinazione <> 23 Then
                    ' Copia i valori
                    wsDestinazione.Cells(rigaDestinazione, 1).Value = wsOrigine.Cells(i, 2).Value
                    wsDestinazione.Cells(rigaDestinazione, 4).Value = wsOrigine.Cells(i, 5).Value
                    wsDestinazione.Cells(rigaDestinazione, 5).Value = wsOrigine.Cells(i, 6).Value
                End If

                ' Aggiungi valori a A24 e U24, gestendo errori di conversione
                valoreC = Trim(wsOrigine.Cells(i, 3).Value)
                If Not IsEmpty(valoreC) Then
                    If Not ValoreEsistente(valoriC, valoreC) Then
                        valoriC.Add valoreC
                        concatenatoA24 = concatenatoA24 & IIf(concatenatoA24 = "", "", vbCrLf) & valoreC
                    End If
                End If

                valoreD = Trim(wsOrigine.Cells(i, 4).Value)
                If Not IsEmpty(valoreD) Then
                    If Not ValoreEsistente(valoriD, valoreD) Then
                        valoriD.Add valoreD
                        concatenatoU24 = concatenatoU24 & IIf(concatenatoU24 = "", "", vbCrLf) & valoreD
                    End If
                End If

                rigaDestinazione = rigaDestinazione + 1
            End If
        Next i

        ' Assegna le concatenazioni alle celle A24 e U24
        wsDestinazione.Range("A24").Value = concatenatoA24
        wsDestinazione.Range("U24").Value = concatenatoU24
    Else
        MsgBox "La cella K4 del foglio 'Elabora Giornaliera' non contiene una data valida.", vbExclamation
    End If

    Application.CutCopyMode = False
    Set valoriC = Nothing
    Set valoriD = Nothing
    Set wsOrigine = Nothing
    Set wsDestinazione = Nothing

End Sub

Function ValoreEsistente(valori As Collection, valore As String) As Boolean
    Dim v As Variant
    On Error Resume Next
    For Each v In valori
        If v = valore Then
            ValoreEsistente = True
            Exit Function
        End If
    Next v
    ValoreEsistente = False
End Function


```

## Componente: Modulo12.bas
Stream: VBA/Modulo12

```vba
Attribute VB_Name = "Modulo12"
Sub SmistaDatiGiorno4()
    Dim wsOrigine As Worksheet, wsDestinazione As Worksheet
    Dim ultimaRiga As Long, i As Long
    Dim data As Date, dataGiorno4 As Date
    Dim rigaDestinazione As Long
    Dim concatenatoA24 As String
    Dim concatenatoU24 As String
    Dim valoreC As String
    Dim valoreD As String
    Dim valoriC As Collection
    Dim valoriD As Collection
    Dim almenoUnaCorrispondenza As Boolean

    ' Imposta i fogli
    Set wsOrigine = ThisWorkbook.Sheets("Elabora Giornaliera")
    Set wsDestinazione = ThisWorkbook.Sheets("4")

    ' Trova l'ultima riga con dati nel foglio di origine
    ultimaRiga = wsOrigine.Cells(Rows.Count, 1).End(xlUp).Row

    ' Inizializza la riga di partenza per le colonne
    rigaDestinazione = 11

    ' Inizializza le celle di destinazione A24 e U24
    concatenatoA24 = ""
    concatenatoU24 = ""

    ' Inizializza le collezioni per rimuovere duplicati
    Set valoriC = New Collection
    Set valoriD = New Collection

    almenoUnaCorrispondenza = False

    'Gestisci potenziale errore in K5
    On Error Resume Next
    dataGiorno4 = DateValue(Worksheets("Elabora Giornaliera").Range("K5").Value)
    On Error GoTo 0

    'Controlla se la conversione della data è fallita
    If IsDate(dataGiorno4) Then
        ' Ciclo attraverso le righe del foglio di origine
        For i = 1 To ultimaRiga
            ' Controlla se la riga è vuota
            If IsEmpty(wsOrigine.Cells(i, 1).Value) Then Exit For

            On Error Resume Next
            data = CDate(Trim(wsOrigine.Cells(i, 1).Value))
            On Error GoTo 0

            ' Controlla se la data è uguale a dataGiorno4
            If data = dataGiorno4 Then
                almenoUnaCorrispondenza = True
                ' Verifica se riga destinazione non è 21 o 23
                If rigaDestinazione <> 21 And rigaDestinazione <> 23 Then
                    ' Copia i valori
                    wsDestinazione.Cells(rigaDestinazione, 1).Value = wsOrigine.Cells(i, 2).Value
                    wsDestinazione.Cells(rigaDestinazione, 4).Value = wsOrigine.Cells(i, 5).Value
                    wsDestinazione.Cells(rigaDestinazione, 5).Value = wsOrigine.Cells(i, 6).Value
                End If

                ' Aggiungi valori a A24 e U24, gestendo errori di conversione
                valoreC = Trim(wsOrigine.Cells(i, 3).Value)
                If Not IsEmpty(valoreC) Then
                    If Not ValoreEsistente(valoriC, valoreC) Then
                        valoriC.Add valoreC
                        concatenatoA24 = concatenatoA24 & IIf(concatenatoA24 = "", "", vbCrLf) & valoreC
                    End If
                End If

                valoreD = Trim(wsOrigine.Cells(i, 4).Value)
                If Not IsEmpty(valoreD) Then
                    If Not ValoreEsistente(valoriD, valoreD) Then
                        valoriD.Add valoreD
                        concatenatoU24 = concatenatoU24 & IIf(concatenatoU24 = "", "", vbCrLf) & valoreD
                    End If
                End If

                rigaDestinazione = rigaDestinazione + 1
            End If
        Next i

        ' Assegna le concatenazioni alle celle A24 e U24
        wsDestinazione.Range("A24").Value = concatenatoA24
        wsDestinazione.Range("U24").Value = concatenatoU24
    Else
        MsgBox "La cella K5 del foglio 'Elabora Giornaliera' non contiene una data valida.", vbExclamation
    End If

    Application.CutCopyMode = False
    Set valoriC = Nothing
    Set valoriD = Nothing
    Set wsOrigine = Nothing
    Set wsDestinazione = Nothing

End Sub

Function ValoreEsistente(valori As Collection, valore As String) As Boolean
    Dim v As Variant
    On Error Resume Next
    For Each v In valori
        If v = valore Then
            ValoreEsistente = True
            Exit Function
        End If
    Next v
    ValoreEsistente = False
End Function


```

## Componente: Modulo13.bas
Stream: VBA/Modulo13

```vba
Attribute VB_Name = "Modulo13"
Sub SmistaDatiGiorno5()
    Dim wsOrigine As Worksheet, wsDestinazione As Worksheet
    Dim ultimaRiga As Long, i As Long
    Dim data As Date, dataGiorno5 As Date
    Dim rigaDestinazione As Long
    Dim concatenatoA24 As String
    Dim concatenatoU24 As String
    Dim valoreC As String
    Dim valoreD As String
    Dim valoriC As Collection
    Dim valoriD As Collection
    Dim almenoUnaCorrispondenza As Boolean

    ' Imposta i fogli
    Set wsOrigine = ThisWorkbook.Sheets("Elabora Giornaliera")
    Set wsDestinazione = ThisWorkbook.Sheets("5")

    ' Trova l'ultima riga con dati nel foglio di origine
    ultimaRiga = wsOrigine.Cells(Rows.Count, 1).End(xlUp).Row

    ' Inizializza la riga di partenza per le colonne
    rigaDestinazione = 11

    ' Inizializza le celle di destinazione A24 e U24
    concatenatoA24 = ""
    concatenatoU24 = ""

    ' Inizializza le collezioni per rimuovere duplicati
    Set valoriC = New Collection
    Set valoriD = New Collection

    almenoUnaCorrispondenza = False

    'Gestisci potenziale errore in K6
    On Error Resume Next
    dataGiorno5 = DateValue(Worksheets("Elabora Giornaliera").Range("K6").Value)
    On Error GoTo 0

    'Controlla se la conversione della data è fallita
    If IsDate(dataGiorno5) Then
        ' Ciclo attraverso le righe del foglio di origine
        For i = 1 To ultimaRiga
            ' Controlla se la riga è vuota
            If IsEmpty(wsOrigine.Cells(i, 1).Value) Then Exit For

            On Error Resume Next
            data = CDate(Trim(wsOrigine.Cells(i, 1).Value))
            On Error GoTo 0

            ' Controlla se la data è uguale a dataGiorno5
            If data = dataGiorno5 Then
                almenoUnaCorrispondenza = True
                ' Verifica se riga destinazione non è 21 o 23
                If rigaDestinazione <> 21 And rigaDestinazione <> 23 Then
                    ' Copia i valori
                    wsDestinazione.Cells(rigaDestinazione, 1).Value = wsOrigine.Cells(i, 2).Value
                    wsDestinazione.Cells(rigaDestinazione, 4).Value = wsOrigine.Cells(i, 5).Value
                    wsDestinazione.Cells(rigaDestinazione, 5).Value = wsOrigine.Cells(i, 6).Value
                End If

                ' Aggiungi valori a A24 e U24, gestendo errori di conversione
                valoreC = Trim(wsOrigine.Cells(i, 3).Value)
                If Not IsEmpty(valoreC) Then
                    If Not ValoreEsistente(valoriC, valoreC) Then
                        valoriC.Add valoreC
                        concatenatoA24 = concatenatoA24 & IIf(concatenatoA24 = "", "", vbCrLf) & valoreC
                    End If
                End If

                valoreD = Trim(wsOrigine.Cells(i, 4).Value)
                If Not IsEmpty(valoreD) Then
                    If Not ValoreEsistente(valoriD, valoreD) Then
                        valoriD.Add valoreD
                        concatenatoU24 = concatenatoU24 & IIf(concatenatoU24 = "", "", vbCrLf) & valoreD
                    End If
                End If

                rigaDestinazione = rigaDestinazione + 1
            End If
        Next i

        ' Assegna le concatenazioni alle celle A24 e U24
        wsDestinazione.Range("A24").Value = concatenatoA24
        wsDestinazione.Range("U24").Value = concatenatoU24
    Else
        MsgBox "La cella K6 del foglio 'Elabora Giornaliera' non contiene una data valida.", vbExclamation
    End If

    Application.CutCopyMode = False
    Set valoriC = Nothing
    Set valoriD = Nothing
    Set wsOrigine = Nothing
    Set wsDestinazione = Nothing

End Sub

Function ValoreEsistente(valori As Collection, valore As String) As Boolean
    Dim v As Variant
    On Error Resume Next
    For Each v In valori
        If v = valore Then
            ValoreEsistente = True
            Exit Function
        End If
    Next v
    ValoreEsistente = False
End Function


```

## Componente: Foglio8.cls
Stream: VBA/Foglio8

```vba
Attribute VB_Name = "Foglio8"
Attribute VB_Base = "0{00020820-0000-0000-C000-000000000046}"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Attribute VB_TemplateDerived = False
Attribute VB_Customizable = True

```

## Componente: Foglio12.cls
Stream: VBA/Foglio12

```vba
Attribute VB_Name = "Foglio12"
Attribute VB_Base = "0{00020820-0000-0000-C000-000000000046}"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Attribute VB_TemplateDerived = False
Attribute VB_Customizable = True

```

## Componente: Foglio13.cls
Stream: VBA/Foglio13

```vba
Attribute VB_Name = "Foglio13"
Attribute VB_Base = "0{00020820-0000-0000-C000-000000000046}"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Attribute VB_TemplateDerived = False
Attribute VB_Customizable = True

```

## Componente: Foglio14.cls
Stream: VBA/Foglio14

```vba
Attribute VB_Name = "Foglio14"
Attribute VB_Base = "0{00020820-0000-0000-C000-000000000046}"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Attribute VB_TemplateDerived = False
Attribute VB_Customizable = True

```

## Componente: Foglio15.cls
Stream: VBA/Foglio15

```vba
Attribute VB_Name = "Foglio15"
Attribute VB_Base = "0{00020820-0000-0000-C000-000000000046}"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Attribute VB_TemplateDerived = False
Attribute VB_Customizable = True

```

## Componente: Foglio16.cls
Stream: VBA/Foglio16

```vba
Attribute VB_Name = "Foglio16"
Attribute VB_Base = "0{00020820-0000-0000-C000-000000000046}"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Attribute VB_TemplateDerived = False
Attribute VB_Customizable = True

```

## Componente: Foglio17.cls
Stream: VBA/Foglio17

```vba
Attribute VB_Name = "Foglio17"
Attribute VB_Base = "0{00020820-0000-0000-C000-000000000046}"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Attribute VB_TemplateDerived = False
Attribute VB_Customizable = True

```

## Componente: Foglio18.cls
Stream: VBA/Foglio18

```vba
Attribute VB_Name = "Foglio18"
Attribute VB_Base = "0{00020820-0000-0000-C000-000000000046}"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Attribute VB_TemplateDerived = False
Attribute VB_Customizable = True

```

## Componente: Foglio19.cls
Stream: VBA/Foglio19

```vba
Attribute VB_Name = "Foglio19"
Attribute VB_Base = "0{00020820-0000-0000-C000-000000000046}"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Attribute VB_TemplateDerived = False
Attribute VB_Customizable = True

```

## Componente: Foglio20.cls
Stream: VBA/Foglio20

```vba
Attribute VB_Name = "Foglio20"
Attribute VB_Base = "0{00020820-0000-0000-C000-000000000046}"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Attribute VB_TemplateDerived = False
Attribute VB_Customizable = True

```

## Componente: Foglio21.cls
Stream: VBA/Foglio21

```vba
Attribute VB_Name = "Foglio21"
Attribute VB_Base = "0{00020820-0000-0000-C000-000000000046}"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Attribute VB_TemplateDerived = False
Attribute VB_Customizable = True

```

## Componente: Foglio22.cls
Stream: VBA/Foglio22

```vba
Attribute VB_Name = "Foglio22"
Attribute VB_Base = "0{00020820-0000-0000-C000-000000000046}"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Attribute VB_TemplateDerived = False
Attribute VB_Customizable = True

```

## Componente: Foglio23.cls
Stream: VBA/Foglio23

```vba
Attribute VB_Name = "Foglio23"
Attribute VB_Base = "0{00020820-0000-0000-C000-000000000046}"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Attribute VB_TemplateDerived = False
Attribute VB_Customizable = True

```

## Componente: Foglio24.cls
Stream: VBA/Foglio24

```vba
Attribute VB_Name = "Foglio24"
Attribute VB_Base = "0{00020820-0000-0000-C000-000000000046}"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Attribute VB_TemplateDerived = False
Attribute VB_Customizable = True

```

## Componente: Foglio25.cls
Stream: VBA/Foglio25

```vba
Attribute VB_Name = "Foglio25"
Attribute VB_Base = "0{00020820-0000-0000-C000-000000000046}"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Attribute VB_TemplateDerived = False
Attribute VB_Customizable = True

```

## Componente: Foglio26.cls
Stream: VBA/Foglio26

```vba
Attribute VB_Name = "Foglio26"
Attribute VB_Base = "0{00020820-0000-0000-C000-000000000046}"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Attribute VB_TemplateDerived = False
Attribute VB_Customizable = True

```

## Componente: Foglio27.cls
Stream: VBA/Foglio27

```vba
Attribute VB_Name = "Foglio27"
Attribute VB_Base = "0{00020820-0000-0000-C000-000000000046}"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Attribute VB_TemplateDerived = False
Attribute VB_Customizable = True

```

## Componente: Foglio28.cls
Stream: VBA/Foglio28

```vba
Attribute VB_Name = "Foglio28"
Attribute VB_Base = "0{00020820-0000-0000-C000-000000000046}"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Attribute VB_TemplateDerived = False
Attribute VB_Customizable = True

```

## Componente: Foglio29.cls
Stream: VBA/Foglio29

```vba
Attribute VB_Name = "Foglio29"
Attribute VB_Base = "0{00020820-0000-0000-C000-000000000046}"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Attribute VB_TemplateDerived = False
Attribute VB_Customizable = True

```

## Componente: Foglio30.cls
Stream: VBA/Foglio30

```vba
Attribute VB_Name = "Foglio30"
Attribute VB_Base = "0{00020820-0000-0000-C000-000000000046}"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Attribute VB_TemplateDerived = False
Attribute VB_Customizable = True

```

## Componente: Foglio31.cls
Stream: VBA/Foglio31

```vba
Attribute VB_Name = "Foglio31"
Attribute VB_Base = "0{00020820-0000-0000-C000-000000000046}"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Attribute VB_TemplateDerived = False
Attribute VB_Customizable = True

```

## Componente: Foglio32.cls
Stream: VBA/Foglio32

```vba
Attribute VB_Name = "Foglio32"
Attribute VB_Base = "0{00020820-0000-0000-C000-000000000046}"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Attribute VB_TemplateDerived = False
Attribute VB_Customizable = True

```

## Componente: Foglio33.cls
Stream: VBA/Foglio33

```vba
Attribute VB_Name = "Foglio33"
Attribute VB_Base = "0{00020820-0000-0000-C000-000000000046}"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Attribute VB_TemplateDerived = False
Attribute VB_Customizable = True

```

## Componente: Foglio34.cls
Stream: VBA/Foglio34

```vba
Attribute VB_Name = "Foglio34"
Attribute VB_Base = "0{00020820-0000-0000-C000-000000000046}"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Attribute VB_TemplateDerived = False
Attribute VB_Customizable = True

```

## Componente: Foglio35.cls
Stream: VBA/Foglio35

```vba
Attribute VB_Name = "Foglio35"
Attribute VB_Base = "0{00020820-0000-0000-C000-000000000046}"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Attribute VB_TemplateDerived = False
Attribute VB_Customizable = True

```

## Componente: Foglio36.cls
Stream: VBA/Foglio36

```vba
Attribute VB_Name = "Foglio36"
Attribute VB_Base = "0{00020820-0000-0000-C000-000000000046}"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Attribute VB_TemplateDerived = False
Attribute VB_Customizable = True

```

## Componente: Foglio37.cls
Stream: VBA/Foglio37

```vba
Attribute VB_Name = "Foglio37"
Attribute VB_Base = "0{00020820-0000-0000-C000-000000000046}"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Attribute VB_TemplateDerived = False
Attribute VB_Customizable = True

```

## Componente: Foglio38.cls
Stream: VBA/Foglio38

```vba
Attribute VB_Name = "Foglio38"
Attribute VB_Base = "0{00020820-0000-0000-C000-000000000046}"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Attribute VB_TemplateDerived = False
Attribute VB_Customizable = True

```

## Componente: Foglio39.cls
Stream: VBA/Foglio39

```vba
Attribute VB_Name = "Foglio39"
Attribute VB_Base = "0{00020820-0000-0000-C000-000000000046}"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Attribute VB_TemplateDerived = False
Attribute VB_Customizable = True

```

## Componente: Foglio40.cls
Stream: VBA/Foglio40

```vba
Attribute VB_Name = "Foglio40"
Attribute VB_Base = "0{00020820-0000-0000-C000-000000000046}"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Attribute VB_TemplateDerived = False
Attribute VB_Customizable = True

```

## Componente: Modulo44.bas
Stream: VBA/Modulo44

```vba
Attribute VB_Name = "Modulo44"
Option Explicit ' Consigliato all'inizio di ogni modulo

Sub EstraiDateUnivoche()
    ' Dichiarazione delle variabili
    Dim cellaValue As Variant
    Dim valoriUnici As Object
    Dim valoreKey As Variant
    Dim ultimaRiga As Long
    Dim ws As Worksheet
    Dim arrDatiIn As Variant
    Dim arrDatiOut() As Variant
    Dim i As Long, outputIdx As Long

    ' Variabili per ottimizzazione e gestione errori
    Dim prevScreenUpdating As Boolean, prevEnableEvents As Boolean, prevCalculation As XlCalculation
    Dim errorOccurred As Boolean
    errorOccurred = False ' Inizializza il flag di errore

    On Error GoTo GestoreErrori

    ' Salva le impostazioni correnti e ottimizza
    prevScreenUpdating = Application.ScreenUpdating
    prevEnableEvents = Application.EnableEvents
    prevCalculation = Application.Calculation
    Application.ScreenUpdating = False
    Application.EnableEvents = False
    Application.Calculation = xlCalculationManual
    Application.StatusBar = "EstraiDateUnivoche: Avvio elaborazione..."

    Set ws = ThisWorkbook.Sheets("Elabora Giornaliera")
    Set valoriUnici = CreateObject("Scripting.Dictionary")
    ultimaRiga = ws.Cells(ws.Rows.Count, "A").End(xlUp).Row

    If ultimaRiga < 1 Then
        Application.StatusBar = "EstraiDateUnivoche: Nessun dato in colonna A da elaborare."
        GoTo RipristinaImpostazioni
    End If

    arrDatiIn = ws.Range("A1:A" & ultimaRiga).Value
    Application.StatusBar = "EstraiDateUnivoche: Analisi di " & ultimaRiga & " righe..."

    For i = LBound(arrDatiIn, 1) To UBound(arrDatiIn, 1)
        cellaValue = arrDatiIn(i, 1)
        If cellaValue <> "" And IsDate(cellaValue) Then
            If Not valoriUnici.Exists(CStr(cellaValue)) Then
                valoriUnici.Add CStr(cellaValue), Nothing
            End If
        End If
    Next i

    If valoriUnici.Count = 0 Then
        Application.StatusBar = "EstraiDateUnivoche: Nessuna data unica trovata."
        GoTo RipristinaImpostazioni
    End If

    ReDim arrDatiOut(1 To valoriUnici.Count, 1 To 1)
    outputIdx = 0
    Application.StatusBar = "EstraiDateUnivoche: Preparazione " & valoriUnici.Count & " date uniche..."

    For Each valoreKey In valoriUnici.Keys
        outputIdx = outputIdx + 1
        arrDatiOut(outputIdx, 1) = CDate(valoreKey)
    Next valoreKey

    Application.StatusBar = "EstraiDateUnivoche: Scrittura date in colonna K..."
    With ws.Range("K2").Resize(outputIdx, 1)
        .Value = arrDatiOut
        .NumberFormat = "dd/mm/yyyy"
    End With

    Application.StatusBar = "EstraiDateUnivoche: Completato. " & valoriUnici.Count & " date uniche scritte."
    Application.Wait Now + TimeValue("00:00:02")

RipristinaImpostazioni:
    Application.ScreenUpdating = prevScreenUpdating
    Application.EnableEvents = prevEnableEvents
    Application.Calculation = prevCalculation
    If Not errorOccurred Then ' Pulisce la barra solo se non ci sono stati errori
        Application.StatusBar = False
    End If
    Set valoriUnici = Nothing
    Set ws = Nothing
    Exit Sub

GestoreErrori:
    errorOccurred = True
    Application.StatusBar = "EstraiDateUnivoche: Errore (" & Err.Number & ") - " & Err.Description
    ' Nessun MsgBox, l'errore rimane nella barra di stato
    Resume RipristinaImpostazioni
End Sub

Sub CancellaColonnaKDaK2()
    Dim ultimaRiga As Long, rngDaCancellare As Range, ws As Worksheet

    Dim prevScreenUpdating As Boolean, prevEnableEvents As Boolean
    Dim errorOccurred As Boolean
    errorOccurred = False

    On Error GoTo GestoreErrori

    prevScreenUpdating = Application.ScreenUpdating
    prevEnableEvents = Application.EnableEvents
    Application.ScreenUpdating = False
    Application.EnableEvents = False
    Application.StatusBar = "CancellaColonnaKDaK2: Avvio cancellazione..."

    Set ws = ThisWorkbook.Sheets("Elabora Giornaliera")
    ultimaRiga = ws.Cells(ws.Rows.Count, "K").End(xlUp).Row

    If ultimaRiga >= 2 Then
        Set rngDaCancellare = ws.Range("K2:K" & ultimaRiga)
        Application.StatusBar = "CancellaColonnaKDaK2: Cancellazione del range " & rngDaCancellare.Address(False, False) & "..."
        rngDaCancellare.ClearContents
        Application.StatusBar = "CancellaColonnaKDaK2: Contenuto colonna K (da K2) cancellato."
    Else
        Application.StatusBar = "CancellaColonnaKDaK2: Nessun dato da cancellare in colonna K (da K2)."
    End If
    Application.Wait Now + TimeValue("00:00:02")

RipristinaImpostazioni:
    Application.ScreenUpdating = prevScreenUpdating
    Application.EnableEvents = prevEnableEvents
    If Not errorOccurred Then
        Application.StatusBar = False
    End If
    Set ws = Nothing
    Set rngDaCancellare = Nothing
    Exit Sub

GestoreErrori:
    errorOccurred = True
    Application.StatusBar = "CancellaColonnaKDaK2: Errore (" & Err.Number & ") - " & Err.Description
    Resume RipristinaImpostazioni
End Sub

Sub caricaPDL()
    Dim cellaValue As Variant
    Dim valoriUnici As Object
    Dim valoreKey As Variant
    Dim ultimaRiga As Long
    Dim ws As Worksheet
    Dim arrDatiIn As Variant
    Dim arrDatiOut() As Variant
    Dim i As Long, outputIdx As Long

    Dim prevScreenUpdating As Boolean, prevEnableEvents As Boolean, prevCalculation As XlCalculation
    Dim errorOccurred As Boolean
    errorOccurred = False

    On Error GoTo GestoreErrori

    prevScreenUpdating = Application.ScreenUpdating
    prevEnableEvents = Application.EnableEvents
    prevCalculation = Application.Calculation
    Application.ScreenUpdating = False
    Application.EnableEvents = False
    Application.Calculation = xlCalculationManual
    Application.StatusBar = "caricaPDL: Avvio elaborazione..."

    Set ws = ThisWorkbook.Sheets("Elabora Giornaliera")
    Set valoriUnici = CreateObject("Scripting.Dictionary")
    ultimaRiga = ws.Cells(ws.Rows.Count, "D").End(xlUp).Row

    If ultimaRiga < 1 Then
        Application.StatusBar = "caricaPDL: Nessun dato in colonna D da elaborare."
        GoTo RipristinaImpostazioni
    End If

    arrDatiIn = ws.Range("D1:D" & ultimaRiga).Value
    Application.StatusBar = "caricaPDL: Analisi di " & ultimaRiga & " righe per PDL..."

    For i = LBound(arrDatiIn, 1) To UBound(arrDatiIn, 1)
        cellaValue = arrDatiIn(i, 1)
        If cellaValue <> "" Then
            If Not valoriUnici.Exists(CStr(cellaValue)) Then
                valoriUnici.Add CStr(cellaValue), Nothing
            End If
        End If
    Next i

    If valoriUnici.Count = 0 Then
        Application.StatusBar = "caricaPDL: Nessun PDL unico trovato."
        GoTo RipristinaImpostazioni
    End If

    ReDim arrDatiOut(1 To valoriUnici.Count, 1 To 1)
    outputIdx = 0
    Application.StatusBar = "caricaPDL: Preparazione " & valoriUnici.Count & " PDL unici..."

    For Each valoreKey In valoriUnici.Keys
        outputIdx = outputIdx + 1
        arrDatiOut(outputIdx, 1) = valoreKey
    Next valoreKey

    Application.StatusBar = "caricaPDL: Scrittura PDL in colonna L..."
    ws.Range("L2").Resize(outputIdx, 1).Value = arrDatiOut

    Application.StatusBar = "caricaPDL: Completato. " & valoriUnici.Count & " PDL unici scritti."
    Application.Wait Now + TimeValue("00:00:02")

RipristinaImpostazioni:
    Application.ScreenUpdating = prevScreenUpdating
    Application.EnableEvents = prevEnableEvents
    Application.Calculation = prevCalculation
    If Not errorOccurred Then
        Application.StatusBar = False
    End If
    Set valoriUnici = Nothing
    Set ws = Nothing
    Exit Sub

GestoreErrori:
    errorOccurred = True
    Application.StatusBar = "caricaPDL: Errore (" & Err.Number & ") - " & Err.Description
    Resume RipristinaImpostazioni
End Sub

Sub CancellaColonnaLDaL2()
    Dim ultimaRiga As Long, cella As Range, rngDaCancellare As Range, ws As Worksheet

    Dim prevScreenUpdating As Boolean, prevEnableEvents As Boolean
    Dim errorOccurred As Boolean
    Dim originalAlertStatus As Boolean ' Per Application.DisplayAlerts
    errorOccurred = False

    On Error GoTo GestoreErrori

    prevScreenUpdating = Application.ScreenUpdating
    prevEnableEvents = Application.EnableEvents
    Application.ScreenUpdating = False
    Application.EnableEvents = False
    Application.StatusBar = "CancellaColonnaLDaL2: Avvio cancellazione..."

    Set ws = ThisWorkbook.Sheets("Elabora Giornaliera")
    ultimaRiga = ws.Cells(ws.Rows.Count, "L").End(xlUp).Row

    If ultimaRiga >= 2 Then
        Set rngDaCancellare = ws.Range("L2:L" & ultimaRiga)
        Application.StatusBar = "CancellaColonnaLDaL2: Rimozione unione celle nel range " & rngDaCancellare.Address(False, False) & "..."

        originalAlertStatus = Application.DisplayAlerts
        Application.DisplayAlerts = False ' Sopprime eventuali avvisi durante UnMerge

        For Each cella In rngDaCancellare
            If cella.MergeCells Then
                cella.UnMerge
            End If
        Next cella

        Application.DisplayAlerts = originalAlertStatus ' Ripristina stato avvisi

        Application.StatusBar = "CancellaColonnaLDaL2: Cancellazione contenuto range " & rngDaCancellare.Address(False, False) & "..."
        rngDaCancellare.ClearContents
        Application.StatusBar = "CancellaColonnaLDaL2: Contenuto colonna L (da L2) cancellato."
    Else
        Application.StatusBar = "CancellaColonnaLDaL2: Nessun dato da cancellare in colonna L (da L2)."
    End If
    Application.Wait Now + TimeValue("00:00:02")

RipristinaImpostazioni:
    Application.ScreenUpdating = prevScreenUpdating
    Application.EnableEvents = prevEnableEvents
    If Not IsMissing(originalAlertStatus) Then ' Assicura che sia stata impostata prima di tentare il ripristino
       If Application.DisplayAlerts <> originalAlertStatus Then Application.DisplayAlerts = originalAlertStatus
    End If
    If Not errorOccurred Then
        Application.StatusBar = False
    End If
    Set ws = Nothing
    Set rngDaCancellare = Nothing
    Set cella = Nothing
    Exit Sub

GestoreErrori:
    errorOccurred = True
    Application.StatusBar = "CancellaColonnaLDaL2: Errore (" & Err.Number & ") - " & Err.Description
    Resume RipristinaImpostazioni
End Sub

```

## Componente: Modulo45.bas
Stream: VBA/Modulo45

```vba
Attribute VB_Name = "Modulo45"
Sub CancellaERinominaFogliOre()

  Dim ws As Worksheet
  Dim dataComeTesto As String
  Dim sheetName As String

  Application.DisplayAlerts = False 'Disable alerts

  For Each ws In ThisWorkbook.Worksheets
    sheetName = ws.Name

    If IsNumeric(sheetName) Then
      Dim sheetNum As Long
      On Error Resume Next
      sheetNum = CLng(sheetName)
      On Error GoTo 0

      If sheetNum >= 1 And sheetNum <= 31 Then

        If IsEmpty(ws.Range("O6").Value) Then
          ws.Delete
        Else
          On Error Resume Next
          dataComeTesto = Format(ws.Range("O6").Value, "dd-mm-yy")
          On Error GoTo 0

          If dataComeTesto = "" Then
            ws.Delete
          Else
            ws.Name = dataComeTesto
          End If
        End If
      End If
    End If
  Next ws

  Application.DisplayAlerts = True 'Re-enable alerts

End Sub



```

## Componente: Modulo46.bas
Stream: VBA/Modulo46

```vba
Attribute VB_Name = "Modulo46"
Option Explicit

Sub ElaboraConsuntivoSquadra()

    Dim wsConsuntivo As Worksheet
    Dim wsDestinazione As Worksheet
    Dim wsRifVBA As Worksheet
    Dim wsInsDati As Worksheet
    Dim wsElabGiorn As Worksheet

    Dim rigaConsuntivo As Long
    Dim colonnaConsuntivo As Long
    Dim valoreCella As Variant
    Dim codiceA As String
    Dim i As Long
    Dim valoreB4 As String
    Dim valoreD6 As String
    Dim valoreP21 As Variant
    Dim risultato As Variant

    ' Variabili per la logica (D13 Inserimento Dati)
    Dim valoreD13 As String
    Dim collUnivoci As Collection
    Dim ultimaRigaElab As Long
    Dim numUnivoci As Long

    ' Variabili per Ordinamento in Memoria
    Dim rngSort As Range
    Dim arrData As Variant
    Dim j As Long, k As Long
    Dim valI As String, valJ As String
    Dim temp As Variant
    Dim swap As Boolean

    ' Imposta i fogli di lavoro
    On Error Resume Next
    Set wsConsuntivo = ThisWorkbook.Sheets("Consuntivo")
    Set wsDestinazione = ThisWorkbook.Sheets("Consuntivo")
    Set wsRifVBA = ThisWorkbook.Sheets("rif.VBA")
    Set wsInsDati = ThisWorkbook.Sheets("inserimento dati")
    Set wsElabGiorn = ThisWorkbook.Sheets("Elabora Giornaliera")
    On Error GoTo 0

    ' Controlli esistenza fogli base
    If wsConsuntivo Is Nothing Or wsRifVBA Is Nothing Then
        MsgBox "Errore: Fogli essenziali ('Consuntivo' o 'rif.VBA') non trovati.", vbCritical
        Exit Sub
    End If

    ' Leggi i valori di controllo da rif.VBA
    valoreB4 = Trim(UCase(wsRifVBA.Range("B4").Value))
    valoreD6 = Trim(UCase(wsRifVBA.Range("D6").Value))

    ' --- OVERRIDE LOGICA: Se CHIAMATA, forza CONSTATAZIONE PURA ---
    If valoreB4 = "CHIAMATA" Then
        valoreD6 = "CONSTATAZIONE PURA"
    End If

    ' 1. GESTIONE SQUADRA (Giornaliera o Settimanale)
    If valoreD6 = "SQUADRA GIORNALIERA" Then
        valoreP21 = wsConsuntivo.Range("P21").Value
        If IsNumeric(valoreP21) Then
            On Error Resume Next
            risultato = CDbl(valoreP21) / 16.5
            On Error GoTo 0
            If Not IsError(risultato) Then
                Call ScriviOAggiornaRiga(wsDestinazione, "14420", risultato)
            Else
                MsgBox "Errore calcolo P21 / 16.5", vbExclamation
            End If
        Else
            MsgBox "Valore P21 non numerico.", vbExclamation
        End If

    ElseIf valoreD6 = "SQUADRA SETTIMANALE" Then
        valoreP21 = wsConsuntivo.Range("P21").Value
        If IsNumeric(valoreP21) Then
            On Error Resume Next
            risultato = CDbl(valoreP21) / 76
            On Error GoTo 0
            If Not IsError(risultato) Then
                Call ScriviOAggiornaRiga(wsDestinazione, "14600", risultato)
            Else
                MsgBox "Errore calcolo P21 / 76", vbExclamation
            End If
        Else
            MsgBox "Valore P21 non numerico.", vbExclamation
        End If
    End If

    ' 2. GESTIONE VOCI ANALITICHE (Chiamata o Constatazione)
    If valoreD6 = "CONSTATAZIONE PURA" Then
        For rigaConsuntivo = 23 To 26
            For colonnaConsuntivo = 15 To 19
                valoreCella = wsConsuntivo.Cells(rigaConsuntivo, colonnaConsuntivo).Value

                If IsNumeric(valoreCella) And valoreCella <> 0 And Not IsEmpty(valoreCella) Then
                    Select Case colonnaConsuntivo
                        Case 15: codiceA = CStr(10660 + (rigaConsuntivo - 23) * 50)
                        Case 16: codiceA = CStr(10670 + (rigaConsuntivo - 23) * 50)
                        Case 17: codiceA = CStr(10690 + (rigaConsuntivo - 23) * 50)
                        Case 18: codiceA = CStr(10680 + (rigaConsuntivo - 23) * 50)
                        Case 19: codiceA = CStr(18030 + (rigaConsuntivo - 23) * 10)
                    End Select

                    Call ScriviOAggiornaRiga(wsDestinazione, codiceA, valoreCella)
                End If
            Next colonnaConsuntivo
        Next rigaConsuntivo
    End If

    ' 3. GESTIONE INDENNITA 10870
    If Not wsInsDati Is Nothing And Not wsElabGiorn Is Nothing Then
        valoreD13 = Trim(UCase(wsInsDati.Range("D13").Value))

        If valoreD13 = "CHIAMATA" Then
            Set collUnivoci = New Collection
            ultimaRigaElab = wsElabGiorn.Cells(wsElabGiorn.Rows.Count, 2).End(xlUp).Row

            If ultimaRigaElab >= 1 Then
                On Error Resume Next
                For i = 1 To ultimaRigaElab
                    Dim valCella As String
                    valCella = Trim(wsElabGiorn.Cells(i, 2).Value)
                    If valCella <> "" Then
                        collUnivoci.Add valCella, CStr(valCella)
                    End If
                Next i
                On Error GoTo 0

                numUnivoci = collUnivoci.Count

                If numUnivoci > 0 Then
                    Call ScriviOAggiornaRiga(wsDestinazione, "10870", numUnivoci)
                End If
            End If
        End If
    End If

    ' 4. ORDINAMENTO FINALE IN MEMORIA (Bubble Sort)
    ' Questo metodo funziona anche se ci sono celle unite, perché riscrive solo i valori.

    Set rngSort = wsDestinazione.Range("A22:F44")
    arrData = rngSort.Value ' Legge tutto in una matrice 23x6

    ' Ciclo di ordinamento (Bubble Sort) basato sulla colonna 1 (Codice)
    For i = 1 To UBound(arrData, 1) - 1
        For j = i + 1 To UBound(arrData, 1)

            valI = Trim(CStr(arrData(i, 1)))
            valJ = Trim(CStr(arrData(j, 1)))

            swap = False

            ' Logica di scambio:
            ' 1. Se I è vuoto e J ha valore -> Scambia (porta i vuoti giù)
            ' 2. Se entrambi hanno valore e I > J -> Scambia (ordine crescente)

            If valI = "" And valJ <> "" Then
                swap = True
            ElseIf valI <> "" And valJ <> "" Then
                If valI > valJ Then swap = True
            End If

            If swap Then
                ' Scambia tutte le colonne (da 1 a 6)
                For k = 1 To 6
                    temp = arrData(i, k)
                    arrData(i, k) = arrData(j, k)
                    arrData(j, k) = temp
                Next k
            End If
        Next j
    Next i

    ' Salva le formule delle colonne B e C per evitare che vengano sovrascritte dai valori
    Dim formuleB As Variant, formuleC As Variant
    formuleB = wsDestinazione.Range("B22:B44").Formula
    formuleC = wsDestinazione.Range("C22:C44").Formula

    ' Scrive i dati ordinati indietro nel foglio
    rngSort.Value = arrData

    ' Ripristina le formule nelle colonne B e C
    wsDestinazione.Range("B22:B44").Formula = formuleB
    wsDestinazione.Range("C22:C44").Formula = formuleC

    Set wsConsuntivo = Nothing
    Set wsDestinazione = Nothing
    Set wsRifVBA = Nothing
    Set wsInsDati = Nothing
    Set wsElabGiorn = Nothing
    Set rngSort = Nothing

End Sub

' --- FUNZIONE HELPER PER GESTIRE DUPLICATI ---
Private Sub ScriviOAggiornaRiga(ws As Worksheet, codice As String, valore As Variant)
    Dim i As Long
    Dim rigaLibera As Long
    Dim rigaTrovata As Long

    rigaLibera = 0
    rigaTrovata = 0

    ' Ciclo nell'area di destinazione A22:A44
    For i = 22 To 44
        ' 1. Cerca se il codice esiste già (confronto stringhe)
        If Trim(CStr(ws.Cells(i, 1).Value)) = Trim(codice) Then
            rigaTrovata = i
            Exit For
        End If

        ' 2. Memorizza la prima riga libera utile
        If rigaLibera = 0 And IsEmpty(ws.Cells(i, 1).Value) Then
            rigaLibera = i
        End If
    Next i

    If rigaTrovata > 0 Then
        ' AGGIORNA riga esistente
        ws.Cells(rigaTrovata, 6).Value = valore
    ElseIf rigaLibera > 0 Then
        ' INSERISCI nuova riga
        ws.Cells(rigaLibera, 1).Value = codice
        ws.Cells(rigaLibera, 6).Value = valore
    Else
        ' Nessuno spazio
        MsgBox "Spazio esaurito nell'area A22:F44 per il codice " & codice, vbExclamation
    End If

End Sub



```

## Componente: Modulo47.bas
Stream: VBA/Modulo47

```vba
Attribute VB_Name = "Modulo47"
Sub EstraiValoriUnivociDaColonnaL()
    Dim ws As Worksheet
    Dim dict As Object
    Dim lastRowL As Long
    Dim rngL As Range
    Dim cell As Range
    Dim valori As Variant
    Dim val As Variant
    Dim outputRow As Long
    Dim valTrim As String

    ' Imposta il foglio di lavoro
    On Error Resume Next
    Set ws = ThisWorkbook.Sheets("Elabora Giornaliera")
    On Error GoTo 0

    If ws Is Nothing Then
        MsgBox "Foglio 'Elabora Giornaliera' non trovato.", vbCritical
        Exit Sub
    End If

    ' Crea un dizionario per memorizzare valori univoci
    Set dict = CreateObject("Scripting.Dictionary")
    ' Imposta la modalità di confronto del testo (case-insensitive)
    dict.CompareMode = vbTextCompare

    ' Trova l'ultima riga compilata nella colonna L
    lastRowL = ws.Cells(ws.Rows.Count, "L").End(xlUp).Row

    ' Se non ci sono dati (solo l'intestazione o meno), esci
    If lastRowL < 2 Then Exit Sub

    ' Definisci l'intervallo di input
    Set rngL = ws.Range("L2:L" & lastRowL)

    ' Pulisci la colonna M (output) prima di scrivere
    ws.Range("M2:M" & ws.Rows.Count).ClearContents

    ' Cicla attraverso ogni cella nella colonna L
    For Each cell In rngL
        If Not IsEmpty(cell.Value) Then
            ' Divide il contenuto della cella in base al carattere "a capo" (vbLf)
            valori = Split(cell.Value, vbLf)

            ' Cicla attraverso i valori splittati
            For Each val In valori
                ' Rimuovi spazi vuoti prima e dopo
                valTrim = Trim(val)

                ' Se il valore non è vuoto e non è già nel dizionario, aggiungilo
                If valTrim <> "" Then
                    If Not dict.Exists(valTrim) Then
                        dict.Add Key:=valTrim, Item:=1
                    End If
                End If
            Next val
        End If
    Next cell

    ' Scrivi i valori univoci dal dizionario alla colonna M
    If dict.Count > 0 Then
        outputRow = 2 ' Riga di partenza per l'output
        For Each val In dict.Keys
            ws.Cells(outputRow, "M").Value = val
            outputRow = outputRow + 1
        Next val
    End If

    ' Pulisci gli oggetti
    Set dict = Nothing
    Set ws = Nothing
End Sub


```

## Componente: Modulo48.bas
Stream: VBA/Modulo48

```vba
Attribute VB_Name = "Modulo48"

Sub TrovaPosizioneMacro()
    Dim VBProj As Object ' VBIDE.VBProject
    Dim VBComp As Object ' VBIDE.VBComponent
    Dim CodeMod As Object ' VBIDE.CodeModule
    Dim macroName As String
    Dim startLine As Long
    Dim startCol As Long
    Dim endLine As Long
    Dim endCol As Long
    Dim found As Boolean

    ' --- Imposta il nome della macro da cercare ---
    macroName = "verificaEstampaFogli"
    ' ----------------------------------------------

    ' NOTA IMPORTANTE:
    ' Per eseguire questo codice, è necessario abilitare l'accesso al modello a oggetti VBA:
    ' 1. Vai su File > Opzioni > Centro protezione
    ' 2. Clicca su "Impostazioni Centro protezione..."
    ' 3. Vai a "Impostazioni macro"
    ' 4. Seleziona la casella "Considera attendibile l'accesso al modello a oggetti dei progetti VBA"
    ' 5. Clicca OK su entrambe le finestre.

    Set VBProj = ThisWorkbook.VBProject
    found = False

    On Error Resume Next ' Ignora errori se un modulo non può essere letto

    For Each VBComp In VBProj.VBComponents
        ' Controlla solo moduli standard (dove solitamente si trovano le macro)
        If VBComp.Type = 1 Then ' 1 = vbext_ct_StdModule
            Set CodeMod = VBComp.CodeModule

            startLine = 1
            startCol = 1
            endLine = CodeMod.CountOfLines
            endCol = 255 ' Lunghezza massima linea (puoi aumentarla se necessario)

            ' Cerca il testo della macro all'interno del modulo
            If CodeMod.Find(Target:=macroName, _
                            startLine:=startLine, StartColumn:=startCol, _
                            endLine:=endLine, EndColumn:=endCol, _
                            WholeWord:=True, MatchCase:=False, PatternSearch:=False) Then

                ' Stampa il risultato nella finestra Immediata (Ctrl+G per vederla)
                Debug.Print "Macro '" & macroName & "' trovata nel modulo: " & VBComp.Name

                ' In alternativa, usa un MsgBox:
                ' MsgBox "Macro '" & macroName & "' trovata nel modulo: " & VBComp.Name

                found = True
                Exit For ' Esce dal ciclo appena trova la prima occorrenza
            End If
        End If
    Next VBComp

    On Error GoTo 0

    If Not found Then
        Debug.Print "Macro '" & macroName & "' non trovata in nessun modulo standard."
        ' MsgBox "Macro '" & macroName & "' non trovata in nessun modulo standard."
    End If

    Set CodeMod = Nothing
    Set VBComp = Nothing
    Set VBProj = Nothing
End Sub




```

## Componente: ModuloFestivi.bas
Stream: VBA/ModuloFestivi

```vba
Attribute VB_Name = "ModuloFestivi"

Option Explicit

Sub AggiornaFestiviAnnuali()
    Dim ws As Worksheet
    Dim sAnno As String
    Dim nAnno As Integer
    Dim colFestivi As Collection
    Dim vData As Variant
    Dim riga As Long
    Dim tbl As ListObject

    ' Target: Foglio inserimento dati
    On Error Resume Next
    Set ws = ThisWorkbook.Sheets("inserimento dati")
    On Error GoTo 0

    If ws Is Nothing Then
        ' Silenzioso all'avvio se il foglio non c'è, o msgbox? Meglio loggare su Immediate
        Debug.Print "Foglio 'inserimento dati' non trovato!"
        Exit Sub
    End If

    ' 1. Ricava anno dal nome file (es. 003-26.xlsm -> 26 -> 2026)
    On Error Resume Next
    Dim baseName As String
    baseName = Left(ThisWorkbook.Name, InStrRev(ThisWorkbook.Name, ".") - 1)
    sAnno = Right(baseName, 2)

    If IsNumeric(sAnno) Then
        nAnno = CInt("20" & sAnno)
    Else
        nAnno = Year(Date) ' Fallback anno corrente
    End If
    On Error GoTo 0

    ' 2. Calcola festivi
    Set colFestivi = GetTuttiFestivi(nAnno)

    ' 3. Scrittura Dati
    ' Tenta di usare Tabella68 se esiste (Se è una ListObject, si adatta da sola alla posizione)
    On Error Resume Next
    Set tbl = ws.ListObjects("Tabella68")
    On Error GoTo 0

    If Not tbl Is Nothing Then
        ' Caso A: Esiste l'oggetto Tabella68
        If tbl.ListRows.Count > 0 Then tbl.DataBodyRange.Delete

        For Each vData In colFestivi
            Dim newRow As ListRow
            Set newRow = tbl.ListRows.Add
            newRow.Range(1, 1).Value = vData
        Next vData
    Else
        ' Caso B: Non esiste tabella, scrivi manualmente partendo da E15
        ' Pulisce l'area da E15 in giù (fino a E60 per sicurezza)
        ws.Range("E15:E60").ClearContents

        riga = 15 ' Nuova posizione richiesta
        For Each vData In colFestivi
            ws.Cells(riga, 5).Value = vData ' Colonna 5 = E
            ws.Cells(riga, 5).NumberFormat = "dd/mm/yyyy"
            riga = riga + 1
        Next vData
    End If

    Debug.Print "Festivi aggiornati per l'anno " & nAnno
End Sub

Private Function GetTuttiFestivi(anno As Integer) As Collection
    Dim c As New Collection
    Dim pasqua As Date
    Dim pasquetta As Date

    ' Fissi
    c.Add DateSerial(anno, 1, 1)   ' Capodanno
    c.Add DateSerial(anno, 1, 6)   ' Epifania
    c.Add DateSerial(anno, 4, 25)  ' Liberazione
    c.Add DateSerial(anno, 5, 1)   ' Lavoro
    c.Add DateSerial(anno, 6, 2)   ' Repubblica
    c.Add DateSerial(anno, 8, 15)  ' Ferragosto
    c.Add DateSerial(anno, 11, 1)  ' Ognissanti
    c.Add DateSerial(anno, 12, 8)  ' Immacolata
    c.Add DateSerial(anno, 12, 13) ' S. Lucia
    c.Add DateSerial(anno, 12, 25) ' Natale
    c.Add DateSerial(anno, 12, 26) ' S. Stefano

    ' Mobili
    pasqua = CalcolaPasqua(anno)
    pasquetta = pasqua + 1

    c.Add pasqua
    c.Add pasquetta

    ' Ordina date
    Set GetTuttiFestivi = OrdinaCollectionDate(c)
End Function

Private Function CalcolaPasqua(anno As Integer) As Date
    Dim a As Integer, b As Integer, c As Integer, d As Integer, e As Integer
    Dim f As Integer, g As Integer, h As Integer, i As Integer, k As Integer
    Dim l As Integer, m As Integer
    a = anno Mod 19
    b = anno \ 100
    c = anno Mod 100
    d = b \ 4
    e = b Mod 4
    f = (b + 8) \ 25
    g = (b - f + 1) \ 3
    h = (19 * a + b - d - g + 15) Mod 30
    i = c \ 4
    k = c Mod 4
    l = (32 + 2 * e + 2 * i - h - k) Mod 7
    m = (a + 11 * h + 22 * l) \ 451
    CalcolaPasqua = DateSerial(anno, (h + l - 7 * m + 114) \ 31, (h + l - 7 * m + 114) Mod 31 + 1)
End Function

Private Function OrdinaCollectionDate(col As Collection) As Collection
    Dim i As Long, j As Long
    Dim temp As Date
    Dim arr() As Date
    Dim res As New Collection

    If col.Count = 0 Then
        Set OrdinaCollectionDate = res
        Exit Function
    End If

    ReDim arr(1 To col.Count)
    For i = 1 To col.Count
        arr(i) = col(i)
    Next i

    For i = 1 To UBound(arr) - 1
        For j = i + 1 To UBound(arr)
            If arr(i) > arr(j) Then
                temp = arr(i)
                arr(i) = arr(j)
                arr(j) = temp
            End If
        Next j
    Next i

    For i = 1 To UBound(arr)
        res.Add arr(i)
    Next i

    Set OrdinaCollectionDate = res
End Function


```

## Componente: Modulo49.bas
Stream: VBA/Modulo49

```vba
Attribute VB_Name = "Modulo49"
Sub ControllaQualificheMancanti()
    Dim tblSource As ListObject
    Dim targetTables As Variant
    Dim cell As Range
    Dim nameToCheck As String
    Dim missingList As String
    Dim isPresent As Boolean
    Dim i As Integer
    Dim destTableToCheck As ListObject
    Dim foundCount As Integer

    ' 1. Imposta la tabella di origine
    On Error Resume Next
    Set tblSource = Range("Tabella2").ListObject
    On Error GoTo 0

    If tblSource Is Nothing Then
        MsgBox "Errore: Tabella2 non trovata.", vbCritical
        Exit Sub
    End If

    ' 2. Lista delle tabelle in cui cercare
    targetTables = Array("Tabella3", "Tabella13", "Tabella134", "Tabella14", "Tabella15")

    missingList = ""
    foundCount = 0

    ' 3. Cicla ogni nome di Tabella2
    For Each cell In tblSource.ListColumns("CognomeNome").DataBodyRange
        nameToCheck = cell.Value
        isPresent = False

        If nameToCheck <> "" Then
            ' Controlla se esiste in una delle tabelle target
            For i = LBound(targetTables) To UBound(targetTables)
                On Error Resume Next
                Set destTableToCheck = Range(targetTables(i)).ListObject
                On Error GoTo 0

                If Not destTableToCheck Is Nothing Then
                    ' Cerca in tutta la tabella (qualsiasi colonna)
                    If Not destTableToCheck.DataBodyRange.Find(What:=nameToCheck, LookIn:=xlValues, LookAt:=xlWhole) Is Nothing Then
                        isPresent = True
                        Exit For ' Trovato, passa al prossimo nome
                    End If
                End If
            Next i

            ' 4. Se non è stato trovato in nessuna tabella, aggiungilo alla lista
            If Not isPresent Then
                missingList = missingList & "- " & nameToCheck & vbNewLine
                foundCount = foundCount + 1
            End If
        End If
    Next cell

    ' 5. Mostra il risultato
    If missingList <> "" Then
        MsgBox "Ci sono " & foundCount & " nomi mancanti nelle tabelle di destinazione:" & vbNewLine & vbNewLine & _
               missingList, vbExclamation, "Nomi da inserire manualmente"
    Else
        MsgBox "Tutti i nomi di Tabella2 sono già presenti nelle altre tabelle.", vbInformation, "Controllo OK"
    End If

End Sub


```
