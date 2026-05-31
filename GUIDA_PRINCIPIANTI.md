# Guida per principianti — ImmunoMind

Tutorial passo-passo per chi usa il simulatore per la prima volta, anche senza esperienza di programmazione.

---

## Cos'è ImmunoMind?

ImmunoMind è un simulatore educativo che mostra come il sistema immunitario reagisce a un'infezione. Puoi osservare cellule e patogeni in movimento, introdurre infezioni, somministrare farmaci e confrontare scenari diversi.

**Non è un software medico:** è uno strumento didattico con regole semplificate ma basate su concetti biologici reali.

---

## Installazione

### 1. Verifica Python

Apri il terminale (Prompt dei comandi su Windows) e digita:

```bash
python --version
```

Se compare una versione `3.8` o superiore, Python è installato. In caso contrario, scaricalo da [python.org/downloads](https://www.python.org/downloads/) e, durante l'installazione, seleziona **Add Python to PATH**.

### 2. Installa le dipendenze

Nella cartella del progetto:

```bash
pip install -r requirements.txt
```

### 3. Verifica l'ambiente (consigliato)

```bash
python test_sistema.py
```

Lo script controlla librerie e file necessari.

### 4. Avvia il simulatore

```bash
python main.py
```

---

## Primo utilizzo

### Step 1 — Home e menu

All'avvio compare la **Home**. Da qui puoi:

- aprire **Scenari** e scegliere il tipo di infezione;
- regolare la **Gravità** (1–5);
- consultare la **Wiki** integrata;
- premere **Start** per iniziare.

`Esc` riporta sempre alla Home durante la simulazione.

### Step 2 — Scegli uno scenario

| Scenario | Cosa simula |
|----------|-------------|
| **Batterica** | Infezione da *E. coli*, risposta innata, antibiotici |
| **Virale** | Infezione virale; gli antibiotici non servono |
| **Vaccino / Memoria** | Anticorpi pre-esistenti, risposta più rapida |
| **Ferita / Infiammazione** | Segnali infiammatori e dinamiche ambientali |

Per il primo tentativo, scegli **Batterica** con gravità **2** e premi **Start**.

### Step 3 — Osserva il flusso sanguigno

Nell'area sinistra vedrai:

- **Globuli rossi** (rosso) — seguono il flusso sanguigno;
- **Neutrofili** (azzurro) — pattugliano e attaccano i patogeni;
- **Macrofagi** (verde acqua) — fagociti più grandi e lenti.

A destra, l'**HUD** mostra popolazioni, temperatura, farmaci e stato dell'infezione.

### Step 4 — Crea un'infezione

**Clic sinistro** nell'area di simulazione (non sull'HUD).

- Scenario **Batterica**: compaiono batteri gialli.
- Scenario **Virale**: compaiono virus arancioni.

I neutrofili li rilevano e li inseguono (chemotassi). Quando un neutrofilo raggiunge un patogeno, può fagocitarlo: il patogeno scompare e il contatore nell'HUD aumenta.

### Step 5 — Usa un farmaco

| Tasto | Farmaco | Quando usarlo |
|-------|---------|---------------|
| `1` | Penicillina | Infezione **batterica** |
| `2` | Oseltamivir | Infezione **virale** (influenza) |
| `3` | Aciclovir | Infezione **virale** (HSV) |

Nell'HUD compaiono concentrazione ed efficacia. Gli antibiotici **non** agiscono sui virus.

### Step 6 — Febbre e infezione grave

Clicca più volte per introdurre molti patogeni. Osserva l'HUD:

- la **temperatura** sale oltre 38 °C;
- lo **stato** passa da SALUTE → INNATA ATTIVA → INFEZIONE GRAVE;
- nuovi neutrofili possono entrare in circolo (reclutamento).

Premi `1` (batterica) o `2`/`3` (virale) per intervenire, oppure `N` per aggiungere 5 neutrofili.

---

## Controlli completi

| Tasto | Azione |
|-------|--------|
| `Spazio` | Pausa / Riprendi |
| `Esc` | Torna alla Home |
| Click sinistro (area sim.) | Aggiunge patogeni |
| `1` / `2` / `3` | Somministra farmaco |
| `N` | +5 neutrofili |
| `+` / `-` | Velocità simulazione (1×–60×) |
| `R` | Reset simulazione |
| `F` | Schermo intero |
| `E` | Esporta dati CSV |

---

## Concetti chiave

### Neutrofili

Prima linea dell'immunità innata. Pattugliano, rilevano patogeni nel raggio configurato, li inseguono e li fagocitano. Hanno una capacità massima di fagocitosi e una durata di vita limitata.

### Batteri e virus

- **Batteri**: si duplicano per divisione binaria (~20 min simulati). Sensibili alla penicillina.
- **Virus**: modello semplificato; replicazione più rapida; richiedono antivirali e risposta adattativa.

### Fagocitosi e chemotassi

La **chemotassi** guida i leucociti verso i patogeni. La **fagocitosi** elimina il patogeno al contatto, con probabilità e tempo di digestione configurati.

### Risposta adattativa

Dopo un certo tempo compaiono **linfociti T** e **B**. I linfociti B producono **anticorpi** che aiutano a neutralizzare i patogeni. Nello scenario **Vaccino / Memoria** la risposta parte già parzialmente attiva.

### Penicillina e antivirali

I farmaci decadono nel tempo (emivita). L'efficacia dipende dalla dose e dal tipo di patogeno.

---

## Domande frequenti

**I globuli rossi eliminano i patogeni?**  
No. Trasportano ossigeno e rendono visibile il flusso sanguigno.

**Perché alcuni neutrofili non attaccano?**  
Sono fuori dal raggio di rilevamento. Clicca più vicino a loro o attendi che si avvicinino.

**Posso simulare un'infezione virale?**  
Sì. Seleziona lo scenario **Virale** dal menu Scenari.

**La simulazione è realistica?**  
I parametri derivano da dati biologici, ma il modello è semplificato (2D, probabilità, soglie). Utile per capire concetti, non per diagnosi.

**Posso modificare i parametri?**  
Sì, in `config.py` (es. `NUM_NEUTROFILI_INIZIALE`, `BATTERIO_TEMPO_DUPLICAZIONE`).

**Come esporto i dati?**  
Durante la simulazione, premi `E`. I CSV vengono salvati in `dati_esportati/`.

---

## Esperimenti consigliati

Dopo questo tutorial, prova gli esperimenti guidati in [SCENARI.md](SCENARI.md):

1. Infezione lieve senza farmaci
2. Infezione grave non trattata
3. Antibiotico precoce vs tardivo
4. Confronto scenario batterico vs virale

---

## Risoluzione problemi

| Problema | Soluzione |
|----------|-----------|
| `python` non riconosciuto | Reinstalla Python con "Add to PATH", riavvia il PC |
| `No module named 'pygame'` | `pip install pygame` |
| Simulazione lenta | Premi `+` per accelerare; riduci `NUM_GLOBULI_ROSSI_INIZIALE` in `config.py` |
| Finestra troppo grande | Modifica `LARGHEZZA` e `ALTEZZA` in `config.py` |
| Nessun CSV con `E` | Lascia girare la simulazione almeno 30 s simulati o aumenta la velocità |

---

## Prossimi passi

1. Esplora tutti gli scenari e i livelli di gravità.
2. Leggi la Wiki in-app (`Esc` → Wiki).
3. Consulta il [README](README.md) per la modalità batch e l'architettura del codice.
4. Prova a modificare parametri in `config.py` e osserva le differenze.

---

## Risorse utili

- [Treccani — Sistema immunitario](https://www.treccani.it/enciclopedia/sistema-immunitario/)
- [Fondazione Veronesi](https://www.fondazioneveronesi.it/)
- Wiki in-app e sezione Riferimenti nel README
