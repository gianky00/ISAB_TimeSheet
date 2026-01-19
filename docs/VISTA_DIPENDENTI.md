# 👥 Gestione Anagrafica e Abilitazioni ISAB

La vista **Dipendenti** di SyncroJob Enterprise non è una semplice lista anagrafica, ma un **modulo di controllo proattivo** progettato per garantire la continuità operativa del personale presso i siti ISAB.

## 🎯 Scopo del Modulo
Il personale esterno che opera in ISAB è soggetto a una regola di sicurezza automatica: **se non viene registrato un accesso fisico al sito per più di 30 giorni consecutivi, l'abilitazione del badge scade.**
La riattivazione di un dipendente "disabilitato" comporta procedure burocratiche lente che possono causare fermi tecnici.

Questo modulo risolve il problema monitorando costantemente il database delle timbrature e segnalando in anticipo chi rischia la disattivazione.

---

## 🛠 Caratteristiche Principali

### 1. Monitoraggio Intelligente (30 Giorni)
Il sistema incrocia l'anagrafica con l'ultimo ingresso registrato nel database `timbrature_Isab.db`.
- **Attivazione Selettiva**: Il monitoraggio si attiva automaticamente solo per i dipendenti che hanno effettuato almeno un accesso nella loro carriera.
- **Logica Semaforica**:
    - 🟢 **Operativi (Verde)**: Ultimo accesso entro gli ultimi 20 giorni.
    - 🟠 **In Scadenza (Arancione)**: Nessun accesso da 21-30 giorni. Finestra critica per pianificare un ingresso "di mantenimento".
    - 🔴 **Scaduti (Rosso)**: Nessun accesso da oltre 30 giorni. Il dipendente deve essere ri-abilitato.

### 2. Interfaccia "High-Impact"
La UI è stata progettata per dare priorità alle informazioni critiche:
- **Colonna SCAD. ISAB**: Posizionata a sinistra nella tabella master, mostra un pallino colorato e il numero di giorni rimanenti prima dello scadere dei 30 giorni. È ordinabile per individuare subito i casi urgenti.
- **Stato ISAB (Card Interactive)**: Tre card dinamiche nel centro della pagina riepilogano il totale di Operativi, In Scadenza e Scaduti. Le card presentano animazioni al passaggio del mouse e ombreggiature profonde per un feedback visivo immediato.
- **Scheda Dettaglio**: Mostra tutti i dati del dipendente, inclusa la data esatta dell'ultimo accesso e il tempo trascorso.

### 3. Notifiche Proattive
- **Allerta all'Avvio**: All'apertura del programma, SyncroJob esegue una scansione silenziosa. Se rileva dipendenti in zona critica (Arancione/Rosso), mostra una notifica Toast riepilogativa.
- **Badge Sidebar**: L'icona "Dipendenti" nel menu laterale mostra costantemente un badge numerico rosso con il totale dei dipendenti che richiedono attenzione (Scaduti + In Scadenza).

---

## 📂 Operazioni e Gestione Dati

### Importazione Anagrafica
È possibile aggiornare l'elenco dei dipendenti caricando un file CSV (`anagrafica_dipendenti.csv`).
- **Requisito**: Il file deve usare il punto e virgola (`;`) come separatore.
- **Campi supportati**: `id_risorsa`, `Cognome`, `Nome`, `Data_nascita`, `Badge`, `Data_assunzione`.
- **Sincronizzazione**: Il software associa automaticamente le timbrature ai dipendenti tramite la combinazione di **Cognome e Nome**.

### Ricerca Rapida
La barra di ricerca superiore permette di filtrare istantaneamente per Nome, Cognome o numero di Badge, facilitando la gestione anche con database di grandi dimensioni.

---

*Documentazione aggiornata al 19 Gennaio 2026*
