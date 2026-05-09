# 🎮 Command Palette V2: Interactive CLI Experience

Obiettivo: Trasformare la palette in un vero terminale interattivo per "Pilotare" SyncroJob senza mouse.

## � Concetto Architetturale: "Conversational UI"

La palette non è più solo una lista piatta, ma una macchina a stati.
Funzionamento:

1. **Root Level**: Comandi globali (es. `Run`, `Go to`, `Settings`).
2. **Flow**: Selezionando un comando "parent" (es. `Run Bot`), la palette **NON SI CHIUDE**.
3. **Child Level**: Mostra le opzioni per quel contesto (es. Lista Bot).
4. **Parameter Level**: Chiede i parametri necessari (es. Date, Opzioni).

## 🌊 Esempio di Flusso: "Scarico Timbrature"

1. **User**: Digita `run`
    * *Palette*:
        * `> Run Task...` (Selezionato)
        * `> Run Diagnostics`
2. **User**: `Enter`
    * *Palette (Input pulito, Breadcrumb: "Run >")*
    * *Lista*:
        * `Scarica Timbrature (Portale)`
        * `Scarica Quadre (DataEase)`
        * `Analisi OdA`
3. **User**: Seleziona `Scarica Timbrature` -> `Enter`
    * *Palette (Breadcrumb: "Run > Timbrature >")*
    * *Lista Parametri*:
        * `Oggi`
        * `Ieri`
        * `Mese Corrente`
        * `Intervallo Custom...`
4. **User**: Seleziona `Oggi` -> `Enter`
    * *Action*: La palette si chiude e il bot parte.

## 🛠️ Tecniche di Implementazione

### 1. `ActionRegistry` & `CommandNode`

Struttura dati ad albero per definire i comandi e le loro dipendenze.

```python
class CommandNode:
    label: str
    action: Callable OR List[CommandNode] # Se lista, è un sottomenu
    fetch_dynamic_options: Callable # Per generare opzioni al volo (es. lista file)
```

### 2. UI Changes (`CommandPaletteDialog`)

- **Breadcrumbs Bar**: Piccola riga sopra l'input per mostrare il percorso (es. `Home > Run > Timbrature`).
* **State Management**: `self.current_node`, `self.history` (per tasto Backspace/Esc per tornare indietro).
* **Dynamic Provider**: Supporto per funzioni che ritornano liste (es. lista dipendenti dal DB per una ricerca rapida).

## � Comandi Pianificati V2

### Menu `Run` (Esecuzione)

- `Timbrature` -> `[Oggi, Ieri, Mese, Custom]`
* `SafeWork` -> `[Scarico PDL, Ricerca Dipendente]`
* `Contabilità` -> `[Importa XML, Analisi OdA, Genera Report]`

### Menu `Go` (Navigazione)

- `Impostazioni` -> `[Tutti i Tab...]`
* `Cartelle` -> `[Log, Output, Config, Temp]`

### Menu `Set` (Modifica Rapida)

- `Cambia Account` -> `[Portale: User1, Portale: User2...]`
* `Tema` -> `[Light, Dark, System]`

## ⚡ UX Rules

1. **Backspace**: Torna al livello precedente.
2. **Esc**: Chiude tutto (o torna alla root se configurato).
3. **Tab**: Autokompleta il comando selezionato.
4. **Icons**: Ogni step ha icone contestuali.
