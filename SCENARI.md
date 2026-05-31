# 🧪 Scenari ed Esperimenti - ImmunoMind

Questa guida ti aiuta a esplorare diversi aspetti del sistema immunitario attraverso esperimenti pratici.

---

## 🔰 Scenario 1: PRIMA INFEZIONE

**Obiettivo**: Osservare la risposta innata a una piccola infezione

### Procedura
1. Avvia ImmunoMind
2. Premi **ESC** per chiudere il menu
3. Clicca **1 volta** nell'area centrale → Aggiungi 3 batteri
4. **OSSERVA** senza intervenire

### Cosa Osservare
- ⏱️ **Tempo di rilevamento**: Quanto impiegano i neutrofili a trovare i batteri?
- 🎯 **Chemotassi**: Vedi i cerchi gialli attorno ai neutrofili in inseguimento?
- 🍽️ **Fagocitosi**: Quando un neutrofilo raggiunge un batterio, questo scompare (fagocitato)
- 📈 **HUD**: Conta batteri diminuisce, batteri fagocitati aumenta
- 🌡️ **Temperatura**: Resta ~37°C (infezione troppo piccola per febbre)

### Risultato Atteso
✅ I neutrofili eliminano tutti i batteri in 1-3 minuti simulati

### Domande di Riflessione
- Quanti neutrofili hanno partecipato all'attacco?
- Quanto tempo è servito per risolvere l'infezione?
- Qualche neutrofilo è morto durante il processo?

---

## ⚠️ Scenario 2: INFEZIONE GRAVE NON TRATTATA

**Obiettivo**: Vedere cosa succede quando i batteri si moltiplicano più velocemente dell'eliminazione

### Procedura
1. Avvia ImmunoMind
2. Clicca **10 volte** rapidamente nell'area di simulazione → 30 batteri
3. **NON USARE antibiotici**
4. Premi **+** per accelerare a 2x o 4x
5. Osserva per 5 minuti reali

### Cosa Osservare
- 📊 **Crescita esponenziale**: Batteri si duplicano ogni 20 min → 30 → 60 → 120
- 🌡️ **Febbre**: Temperatura sale gradualmente sopra 38°C
- 🔵 **Reclutamento**: Nuovi neutrofili appaiono dall'alto (richiamo dal midollo)
- ⚖️ **Equilibrio**: Si raggiunge uno stallo o i batteri vincono?
- 🟡→🔴 **Stato HUD**: Da "INNATA ATTIVA" a "INFEZIONE GRAVE"

### Risultato Atteso
⚠️ Infezione continua a crescere, sistema immunitario in difficoltà

### Domande di Riflessione
- A che punto l'infezione è diventata incontrollabile?
- Il reclutamento di nuovi neutrofili è stato sufficiente?
- Cosa succederebbe in un corpo reale? (Risposta: serve intervento medico!)

---

## 💊 Scenario 3: TRATTAMENTO ANTIBIOTICO PRECOCE

**Obiettivo**: Dimostrare l'importanza del trattamento tempestivo

### Procedura
1. Avvia ImmunoMind
2. Clicca **5 volte** → 15 batteri
3. **SUBITO** premi **1** (Penicillina)
4. Osserva

### Cosa Osservare
- 💊 **HUD Farmaci**: Concentrazione Penicillina = 100 mg/L, Efficacia = 85%
- 💀 **Mortalità batterica**: Batteri muoiono più velocemente (antibiotico + neutrofili)
- 📉 **Curva decrescente**: Popolazione batterica crolla rapidamente
- ⏱️ **Tempo risoluzione**: 2-4 minuti simulati
- 🌡️ **No febbre**: Temperatura resta normale

### Risultato Atteso
✅ Infezione risolta rapidamente, sistema immunitario vince facilmente

---

## 🚨 Scenario 4: TRATTAMENTO ANTIBIOTICO TARDIVO

**Obiettivo**: Confrontare efficacia trattamento precoce vs tardivo

### Procedura
1. Avvia ImmunoMind
2. Clicca **10 volte** → 30 batteri
3. **ASPETTA** 3 minuti reali (batteri si moltiplicano)
4. **POI** premi **1** (Penicillina)
5. Osserva HUD

### Cosa Osservare
- 🔴 **Popolazione**: Ora ci sono 50-100+ batteri
- 💊 **Efficacia relativa**: Antibiotico efficace MA...
- ⏱️ **Tempo risoluzione**: MOLTO più lungo (10-15 min simulati)
- 🌡️ **Febbre**: Temperatura alta (38-39°C)
- 🔵 **Sforzo immunitario**: Molti neutrofili muoiono

### Risultato Atteso
⚠️ Infezione risolta MA con molto più "danno" al sistema

### Confronto con Scenario 3
| Parametro | Precoce | Tardivo |
|-----------|---------|---------|
| Tempo risoluzione | 2-4 min | 10-15 min |
| Neutrofili persi | 2-5 | 15-30 |
| Febbre | No | Sì |
| Stress sistema | Basso | Alto |

**Lezione**: "L'antibiotico funziona sempre" ✅ → "Ma usarlo presto è MOLTO meglio" ⭐

---

## 🔬 Scenario 5: CICLO VITA NEUTROFILO

**Obiettivo**: Seguire un singolo neutrofilo dalla nascita alla morte

### Procedura
1. Avvia ImmunoMind
2. Premi **R** per reset
3. Identifica un neutrofilo (cerchio azzurro)
4. Seguilo con lo sguardo
5. Clicca vicino a lui per aggiungere batteri

### Cosa Osservare
- 🔵 **Stato pattuglia**: Movimento casuale
- 👁️ **Rilevamento**: Cerchio giallo appare (ha "visto" batterio)
- 🏃 **Inseguimento**: Movimento diretto verso batterio
- 🍽️ **Fagocitosi**: Ferma per 20 sec (sta digerendo)
- 🔁 **Ripete**: Torna a pattuglia o cerca altro batterio
- ☠️ **Morte**: Dopo ~5 min simulati (o 10 batteri fagocitati)

### Contatore nell'HUD
- "Batteri fagocitati" aumenta quando il neutrofilo muore (rilascia conteggio)

---

## 🧬 Scenario 6: CRESCITA BATTERICA PURA

**Obiettivo**: Osservare crescita esponenziale senza interferenze

### Procedura
1. Avvia ImmunoMind
2. Premi **R** per reset
3. Clicca nell'angolo in alto a sinistra → Aggiungi 3 batteri
4. **Premi N 20 volte** per rimuovere tutti i neutrofili (bug divertente: in realtà li aggiungi, ignora!)
   
   **ALTERNATIVA**: Modifica `config.py` → `NUM_NEUTROFILI_INIZIALE = 0`

5. Osserva la crescita

### Cosa Osservare
- 📈 **Duplicazione**: 3 → 6 → 12 → 24 → 48...
- ⏱️ **Tempo raddoppio**: Esattamente 20 minuti simulati
- 🌡️ **Temperatura**: Sale comunque (batteri rilasciano tossine)
- 📊 **Modello esponenziale**: N(t) = N₀ × 2^(t/20)

### Calcolo Teorico
- **t=0**: 3 batteri
- **t=20min**: 6 batteri
- **t=40min**: 12 batteri
- **t=60min**: 24 batteri
- **t=120min**: 96 batteri

### Applicazione Reale
Questo spiega perché infezioni possono diventare pericolose RAPIDAMENTE se non trattate!

---

## 💉 Scenario 7: EFFETTO DOSE ANTIBIOTICO

**Obiettivo**: Confrontare singola dose vs dosi multiple

### Esperimento A: Dose Singola
1. Reset
2. Clicca 8 volte → 24 batteri
3. Premi **1** una volta
4. Osserva concentrazione Penicillina nell'HUD
5. Nota: Decade da 100 → 50 → 25 → ... (emivita 30 min)

### Esperimento B: Dosi Multiple
1. Reset
2. Clicca 8 volte → 24 batteri
3. Premi **1** tre volte (ogni 30 sec)
4. Osserva: Concentrazione = 300 mg/L, Efficacia > 100% (cappata a 100%)

### Confronto
- Dose singola: Infezione risolta in ~8 min
- Dosi multiple: Infezione risolta in ~3 min

**Lezione medica**: Mantenere concentrazione farmaco costante è importante (ecco perché "prendi antibiotico ogni 8 ore"!)

---

## 🎯 Scenario 8: STRESS TEST

**Obiettivo**: Testare i limiti del sistema immunitario

### Procedura
1. Avvia ImmunoMind
2. Premi **+++ ** per velocità 8x o 16x
3. Clicca ripetutamente OVUNQUE → 100+ batteri
4. Osserva il caos!
5. Quando vuoi, premi **1** ripetutamente

### Cosa Osservare
- 🌡️ **Febbre massima**: ~38.5°C
- 🔵 **Reclutamento intenso**: Neutrofili appaiono continuamente
- 💊 **Necessità farmaci**: Impossibile vincere solo con sistema immunitario
- 🔴 **Infezione sistemica**: Tutto lo schermo è giallo!

### Challenge
Riesci a salvare il "paziente"? Quante dosi di Penicillina servono?

---

## 📚 Esperimenti Avanzati

### 🧪 Esperimento: Emivita Farmaco

**Domanda**: Quanto decade la Penicillina nel tempo?

**Metodo**:
1. Reset
2. NON aggiungere batteri
3. Premi **1** (100 mg/L)
4. Ogni 30 sec simulati, annota concentrazione nell'HUD

**Risultato atteso**:
```
t=0:    100 mg/L
t=30s:   50 mg/L
t=60s:   25 mg/L
t=90s:   12.5 mg/L
```

**Formula**: C(t) = C₀ × 0.5^(t/emivita)

---

### 🧪 Esperimento: Capacità Fagocitica

**Domanda**: Quanti batteri può uccidere un singolo neutrofilo?

**Metodo**:
1. Modifica `config.py` → `NUM_NEUTROFILI_INIZIALE = 1`
2. Avvia, aggiungi 20 batteri vicino al neutrofilo
3. Conta quanti fagocita prima di morire

**Risposta teorica**: 10 (valore in `NEUTROFILO_CAPACITA_FAGOCITOSI`)

---

### 🧪 Esperimento: Soglia Febbre

**Domanda**: Quanti batteri servono per causare febbre?

**Metodo**:
1. Aggiungi batteri uno alla volta
2. Osserva temperatura nell'HUD
3. Nota quando supera 37.5°C

**Risposta**: >10 batteri (vedi `ambiente.py` riga 37)

---

## 🏆 Sfide per Studenti

### Sfida 1: Medico Efficiente
- Risolvi infezione da 30 batteri usando SOLO 1 dose di Penicillina
- Tempo massimo: 5 minuti simulati

### Sfida 2: Sistema Immunitario Naturale
- Risolvi infezione da 10 batteri SENZA farmaci
- Puoi aggiungere neutrofili con **N**

### Sfida 3: Pandemia
- Sopravvivi a 50 batteri iniziali
- Usa qualsiasi mezzo necessario
- "Vittoria" = 0 batteri entro 10 min simulati

---

## 🎓 Domande per Discussione in Classe

1. **Perché i neutrofili muoiono dopo aver fagocitato molti batteri?**
   - Risposta: Stress ossidativo, accumulo tossine batteriche

2. **Come fanno i neutrofili a "trovare" i batteri?**
   - Risposta: Chemotassi (seguono gradienti chimici come citochine)

3. **Perché la febbre si sviluppa durante infezioni?**
   - Risposta: Citochine infiammatorie (IL-1, IL-6) → ipotalamo aumenta temperatura

4. **Gli antibiotici uccidono direttamente i batteri?**
   - Risposta: Dipende! Batteriostatici (fermano crescita) vs battericidi (uccidono)
   - Penicillina è battericida (rompe parete cellulare → lisi osmotica)

5. **Cosa succederebbe se usassimo antibiotici per infezioni virali?**
   - Risposta: NON funzionano (virus non hanno parete batterica), + rischio resistenza

6. **Perché è importante finire il ciclo antibiotico anche se ti senti meglio?**
   - Risposta: Batteri residui possono rivivere e sviluppare resistenza

---

## 🔮 Scenari Futuri (Fase 2)

Una volta implementati linfociti e virus, potremo simulare:

- 💉 **Vaccinazione**: Memoria immunitaria + risposta secondaria
- 🦠 **Infezione virale**: Linfociti T uccidono cellule infette
- 🧬 **Produzione anticorpi**: Linfociti B + opsonizzazione
- 🔁 **Reinfezione**: Confronto prima vs seconda esposizione

---

**Buon divertimento con gli esperimenti! 🧬🔬**

*Ricorda: Questo è un modello semplificato. Il sistema immunitario reale è MOLTO più complesso e affascinante!*

