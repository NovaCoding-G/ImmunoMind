# Guided Experiments — ImmunoMind

[Italiano](#italiano) · [English](#english)

Hands-on labs to explore innate immunity, antibiotics, fever, and system limits.

---

## Italiano

### Come usare questa guida

1. Avvia con `python main.py`
2. Scegli scenario e gravità dal menu, poi **Start**
3. Usa i controlli descritti nel [README](README.md)

> **Nota:** modello didattico semplificato, non software medico.

---

### 1. Prima infezione

**Obiettivo:** osservare la risposta innata a una piccola infezione.

1. Scenario **Batterica**, gravità 1
2. Clic **1 volta** nell’area di simulazione (~3 batteri)
3. Osserva senza intervenire

**Osserva:** chemotassi (cerchi gialli), fagocitosi, conteggio batteri in HUD, temperatura ~37 °C.

**Risultato atteso:** clearance in 1–3 minuti simulati.

---

### 2. Infezione grave non trattata

**Obiettivo:** crescita batterica vs capacità immunitaria.

1. Clic **10 volte** rapidamente (~30 batteri)
2. **Non** usare antibiotici
3. Accelera con `+` (2×–4×)

**Osserva:** duplicazione batterica, febbre, reclutamento neutrofili, HUD da “innata attiva” a “infezione grave”.

**Risultato atteso:** infezione difficile da controllare senza farmaci.

---

### 3. Antibiotico precoce vs tardivo

**Esperimento A — precoce**

1. Clic **5 volte** (~15 batteri)
2. Subito premi **`1`** (Penicillina)

**Esperimento B — tardivo**

1. Clic **10 volte** (~30 batteri)
2. Aspetta ~3 minuti reali, poi premi **`1`**

| Parametro | Precoce | Tardivo |
|-----------|---------|---------|
| Tempo risoluzione | 2–4 min sim. | 10–15 min sim. |
| Febbre | Rara | Frequente |
| Stress immunitario | Basso | Alto |

**Lezione:** l’antibiotico funziona, ma **prima è meglio**.

---

### 4. Ciclo di vita del neutrofilo

1. Premi **`R`** (reset)
2. Segui un neutrofilo (cerchio azzurro)
3. Aggiungi batteri vicino a lui

**Osserva:** pattuglia → rilevamento → inseguimento → digestione (~20 s) → morte dopo ~5 min sim. o molte fagocitosi.

---

### 5. Crescita batterica pura

**Obiettivo:** modello esponenziale senza interferenze immunitarie.

1. In `config.py` imposta `NUM_NEUTROFILI_INIZIALE = 0` (opzionale)
2. Reset, aggiungi **3 batteri** in un angolo
3. Osserva: 3 → 6 → 12 → 24… (raddoppio ~20 min sim.)

---

### 6. Dose singola vs dosi multiple

**A:** 8 clic (~24 batteri), **`1`** una volta — concentrazione decade (emivita ~30 min sim.)

**B:** stessa infezione, **`1`** tre volte a distanza di ~30 s — clearance più rapida

**Lezione:** mantenere la concentrazione del farmaco conta (come negli schemi “ogni 8 ore”).

---

### 7. Stress test

1. Velocità **`+++`** (8×–16×)
2. Clic ripetuti ovunque (100+ batteri)
3. Intervieni con **`1`** quando serve

**Challenge:** quante dosi servono per “salvare il paziente”?

---

### 8. Esperimenti avanzati

| Domanda | Metodo | Indizio |
|---------|--------|---------|
| Emivita penicillina | Reset, **`1`**, nessun batterio, annota HUD ogni 30 s sim. | C(t) = C₀ × 0.5^(t/emivita) |
| Capacità fagocitica | `NUM_NEUTROFILI_INIZIALE = 1`, 20 batteri vicini | ~10 in `NEUTROFILO_CAPACITA_FAGOCITOSI` |
| Soglia febbre | Aggiungi batteri uno a uno | >10 batteri in `environment.py` |

---

### Sfide per studenti

1. **Medico efficiente:** 30 batteri, **1 sola** dose di penicillina, risoluzione < 5 min sim.
2. **Solo immunità innata:** 10 batteri, **nessun** farmaco (puoi usare **`N`**).
3. **Pandemia:** 50 batteri iniziali, vittoria = 0 batteri entro 10 min sim.

---

## English

### How to use this guide

1. Launch with `python main.py`
2. Pick scenario and severity from the menu, then **Start**
3. See controls in the [README](README.md)

> **Note:** simplified teaching model, not medical software.

---

### 1. First infection

**Goal:** observe innate response to a small infection.

1. **Bacterial** scenario, severity 1
2. **Click once** in the simulation area (~3 bacteria)
3. Watch without intervening

**Watch for:** chemotaxis (yellow rings), phagocytosis, bacterial count in HUD, temperature ~37 °C.

**Expected:** clearance in 1–3 simulated minutes.

---

### 2. Severe untreated infection

**Goal:** bacterial growth vs immune capacity.

1. **Click 10 times** quickly (~30 bacteria)
2. **Do not** use antibiotics
3. Speed up with `+` (2×–4×)

**Watch for:** bacterial doubling, fever, neutrophil recruitment, HUD shifting to “severe infection”.

**Expected:** infection hard to control without drugs.

---

### 3. Early vs late antibiotic

**Experiment A — early**

1. **5 clicks** (~15 bacteria)
2. Immediately press **`1`** (Penicillin)

**Experiment B — late**

1. **10 clicks** (~30 bacteria)
2. Wait ~3 real minutes, then press **`1`**

| Parameter | Early | Late |
|-----------|-------|------|
| Resolution time | 2–4 sim. min | 10–15 sim. min |
| Fever | Unlikely | Common |
| Immune stress | Low | High |

**Takeaway:** antibiotics work, but **timing matters**.

---

### 4. Neutrophil life cycle

1. Press **`R`** (reset)
2. Track one neutrophil (blue circle)
3. Add bacteria nearby

**Watch for:** patrol → detection → chase → digestion (~20 s) → death after ~5 sim. min or many phagocytoses.

---

### 5. Pure bacterial growth

**Goal:** exponential model without immune interference.

1. Set `NUM_NEUTROFILI_INIZIALE = 0` in `config.py` (optional)
2. Reset, add **3 bacteria** in a corner
3. Observe: 3 → 6 → 12 → 24… (doubling ~20 sim. min)

---

### 6. Single dose vs multiple doses

**A:** 8 clicks (~24 bacteria), **`1`** once — concentration decays (half-life ~30 sim. min)

**B:** same load, **`1`** three times ~30 s apart — faster clearance

**Takeaway:** maintaining drug concentration matters (like real “every 8 hours” schedules).

---

### 7. Stress test

1. Speed **`+++`** (8×–16×)
2. Click repeatedly everywhere (100+ bacteria)
3. Rescue with **`1`** as needed

**Challenge:** how many doses to “save the patient”?

---

### 8. Advanced experiments

| Question | Method | Hint |
|----------|--------|------|
| Penicillin half-life | Reset, **`1`**, no bacteria, log HUD every 30 sim. s | C(t) = C₀ × 0.5^(t/half-life) |
| Phagocytic capacity | `NUM_NEUTROFILI_INIZIALE = 1`, 20 nearby bacteria | ~10 in `NEUTROFILO_CAPACITA_FAGOCITOSI` |
| Fever threshold | Add bacteria one by one | >10 bacteria in `environment.py` |

---

### Student challenges

1. **Efficient clinician:** 30 bacteria, **one** penicillin dose, resolve in < 5 sim. min.
2. **Innate immunity only:** 10 bacteria, **no** drugs (you may use **`N`**).
3. **Pandemic:** 50 initial bacteria, win = 0 bacteria within 10 sim. min.

---

© 2026 G.Roscino / NovaCoding — [ImmunoMind](https://github.com/NovaCoding-G/ImmunoMind)
