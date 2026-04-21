#ControMonta

**ControMonta** è una Web App sviluppata in Python e Streamlit dedicata all'ingegneria strutturale. Il software automatizza il calcolo della **contromonta di officina** partendo dagli output di calcolo FEM (es. Midas Civil), permettendo di combinare diversi casi di carico con coefficienti personalizzati e di gestire correttamente i nodi di appoggio (pile/spalle).

## 🚀 Funzionalità Principali

- **Analisi Automatica Conci**: Identifica i nodi dei conci basandosi direttamente sui dati di spostamento forniti.
- **Combinazioni di Carico Dinamiche**: Permette di selezionare quali casi di carico (G, P, Ritiro, ecc.) sommare e con quali coefficienti moltiplicativi.
- **Gestione Appoggi (Pile)**: Possibilità di forzare la monta a zero su nodi specifici definiti dall'utente, garantendo la congruenza fisica del profilo.
- **Output per l'Officina**: Genera una tabella di sintesi con valori di monta arrotondati all'intero (mm), pronta per la produzione.
- **Visualizzazione Interattiva**: Grafico dinamico del profilo di contromonta con evidenza degli appoggi.

## 🛠️ Requisiti Tecnici

L'applicativo richiede Python 3.8+ e le seguenti librerie:
- `streamlit`: Per l'interfaccia utente web.
- `pandas`: Per la manipolazione dei dati.
- `plotly`: Per i grafici interattivi.
- `openpyxl`: Per la lettura dei file Excel (.xlsx).

## 📦 Installazione

1. **Clona o scarica il progetto** sul tuo computer.
2. **Installa le dipendenze** tramite terminale:
   ```bash
   pip install streamlit pandas plotly openpyxl
   ```

## 🏃 Come Avviare l'App

Posizionati nella cartella del progetto col terminale e lancia il comando:
```bash
streamlit run app.py
```
L'interfaccia verrà aperta automaticamente nel tuo browser predefinito.

## 📄 Formato dei Dati di Input (Excel)

Il file Excel caricato deve contenere almeno i seguenti fogli:

1. **`Nodi`**: Deve contenere le colonne `Node` e `X` (coordinata longitudinale).
2. **`disp`**: Deve contenere gli spostamenti verticali esportati dal software FEM. 
   - Colonne richieste: `Node`, `Load` (Nome del caso di carico), `DZ (mm)`.
3. **`Elementi`** (Opzionale): Utilizzato per verifiche di connettività dei nodi.

## 📖 Guida all'Uso

1. **Caricamento**: Trascina il file Excel nella sidebar di sinistra.
2. **Filtro Range**: Seleziona l'intervallo di nodi da considerare (es. per separare Tratto Dx e Tratto Sx).
3. **Definizione Pile**: Inserisci i numeri dei nodi in corrispondenza degli appoggi per forzare la monta a zero.
4. **Configurazione Carichi**: 
   - Seleziona i casi di carico dal menu a tendina.
   - Inserisci il coefficiente per ogni carico (es. `1.0` per Peso Proprio, `0.25` per i mobili).
5. **Calcolo**: Clicca su "Calcola Monta" per generare la tabella e il grafico.
6. **Esportazione**: Scarica il report finale in formato CSV cliccando sul pulsante dedicato.

## 🏗️ Struttura del Progetto

- `app.py`: Gestisce l'interfaccia utente, i widget e la visualizzazione.
- `src.py`: Contiene la logica di calcolo, il pivot dei dati e la generazione del grafico.

---

### Note sul Calcolo della Monta
Il software calcola la monta come l'opposto della somma pesata degli spostamenti verticali:
$$Monta = - \sum (Spostamento_i \times Coefficiente_i)$$
Il valore finale viene **arrotondato all'intero** per facilitare le operazioni di tracciamento in officina.# ControMonta
monta di officina per conci strutturali in carpenteria metallica
