#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ImmunoMind — simulazioni batch senza interfaccia grafica.

Utile per raccogliere molti run in CSV e confrontarli dopo.
Esempio: python run_experiment.py --durata 7200 --repliche 10

Sviluppato da G.Roscino · NovaCoding
© 2026 G.Roscino / NovaCoding. Tutti i diritti riservati.
"""

import argparse
import random

from brand import MARCHIO, AUTORE, COPYRIGHT
from config import RANDOM_SEED, FPS
from environment import Ambiente, GestoreFarmaci
from entities import GlobuloRosso, Neutrofilo, Batterio, Macrofago, LinfocitaT, LinfocitaB
from analytics import SimulationLogger


class SimulationCore:
    """Stessa logica del simulatore, ma senza finestra Pygame — solo numeri e CSV."""

    def __init__(self, seed: int | None = None):
        if seed is None:
            self.seed = RANDOM_SEED if RANDOM_SEED is not None else random.randint(0, 1_000_000)
        else:
            self.seed = seed
        random.seed(self.seed)

        self.ambiente = Ambiente()
        self.gestore_farmaci = GestoreFarmaci()

        self.globuli_rossi: list[GlobuloRosso] = []
        self.neutrofili: list[Neutrofilo] = []
        self.macrofagi: list[Macrofago] = []
        self.linfo_t: list[LinfocitaT] = []
        self.linfo_b: list[LinfocitaB] = []
        self.batteri: list[Batterio] = []

        self.tempo_simulato = 0.0
        self.batteri_fagocitati_totali = 0

        self.logger = SimulationLogger(run_id=str(self.seed), enabled=True)

        from config import (
            NUM_GLOBULI_ROSSI_INIZIALE,
            NUM_NEUTROFILI_INIZIALE,
            NUM_BATTERI_INIZIALE,
            AREA_SIMULAZIONE_X,
            AREA_SIMULAZIONE_Y,
        )

        for _ in range(NUM_GLOBULI_ROSSI_INIZIALE):
            x = random.randint(50, AREA_SIMULAZIONE_X - 50)
            y = random.randint(50, AREA_SIMULAZIONE_Y - 50)
            self.globuli_rossi.append(GlobuloRosso(x, y))

        for _ in range(NUM_NEUTROFILI_INIZIALE):
            x = random.randint(50, AREA_SIMULAZIONE_X - 50)
            y = random.randint(50, AREA_SIMULAZIONE_Y - 50)
            self.neutrofili.append(Neutrofilo(x, y))

        for _ in range(max(2, NUM_NEUTROFILI_INIZIALE // 4)):
            x = random.randint(50, AREA_SIMULAZIONE_X - 50)
            y = random.randint(50, AREA_SIMULAZIONE_Y - 50)
            self.macrofagi.append(Macrofago(x, y))

        for _ in range(NUM_BATTERI_INIZIALE):
            x = random.randint(100, AREA_SIMULAZIONE_X - 100)
            y = random.randint(100, AREA_SIMULAZIONE_Y - 100)
            self.batteri.append(Batterio(x, y))

    def _raccogli_statistiche(self) -> dict:
        from config import LIMITE_ANTICORPI

        return {
            "globuli_rossi": len(self.globuli_rossi),
            "neutrofili": len(self.neutrofili),
            "macrofagi": len(self.macrofagi),
            "linfo_t": len(self.linfo_t),
            "linfo_b": len(self.linfo_b),
            "batteri": len(self.batteri),
            "batteri_fagocitati": self.batteri_fagocitati_totali,
            "temperatura": self.ambiente.temperatura,
            "ossigeno": self.ambiente.ossigeno,
            "concentrazione_penicillina": self.gestore_farmaci.ottieni_concentrazione_totale(
                "penicillina"
            ),
            "efficacia_antibiotico": self.gestore_farmaci.ottieni_efficacia_antibiotico(),
            "anticorpi": self.ambiente.anticorpi,
            "tempo_simulato": self.tempo_simulato,
            "anticorpi_norm": min(1.0, self.ambiente.anticorpi / LIMITE_ANTICORPI),
        }

    def step(self, dt: float) -> None:
        """Un passo di simulazione (senza grafica)."""
        from config import (
            TEMPO_ATTIVAZIONE_ADATTATIVA,
            LIMITE_ANTICORPI,
            AREA_SIMULAZIONE_X,
            AREA_SIMULAZIONE_Y,
        )

        self.tempo_simulato += dt

        self.ambiente.aggiorna(dt, len(self.batteri))
        self.ambiente.dissipa_citochine(dt)

        self.gestore_farmaci.aggiorna(dt)
        efficacia_antibiotico = self.gestore_farmaci.ottieni_efficacia_antibiotico()

        for gr in self.globuli_rossi:
            gr.aggiorna(dt, self.ambiente)

        for n in self.neutrofili:
            n.rileva_patogeni(self.batteri)
            n.aggiorna(dt, self.ambiente)
        morti_n = [n for n in self.neutrofili if not n.vivo]
        for n in morti_n:
            self.batteri_fagocitati_totali += n.batteri_fagocitati
            self.neutrofili.remove(n)

        for m in self.macrofagi:
            m.rileva_patogeni(self.batteri)
            m.aggiorna(dt, self.ambiente)
        self.macrofagi = [m for m in self.macrofagi if m.vivo]

        if self.tempo_simulato > TEMPO_ATTIVAZIONE_ADATTATIVA and self.batteri:
            if len(self.linfo_t) < 10 and random.random() < 0.01:
                x = random.randint(50, AREA_SIMULAZIONE_X - 50)
                y = random.randint(50, AREA_SIMULAZIONE_Y - 50)
                self.linfo_t.append(LinfocitaT(x, y))
            if len(self.linfo_b) < 8 and random.random() < 0.008:
                x = random.randint(50, AREA_SIMULAZIONE_X - 50)
                y = random.randint(50, AREA_SIMULAZIONE_Y - 50)
                self.linfo_b.append(LinfocitaB(x, y))

        for lt in list(self.linfo_t):
            lt.aggiorna(dt, self.ambiente, self.batteri)
            if not lt.vivo:
                self.linfo_t.remove(lt)

        for lb in list(self.linfo_b):
            lb.aggiorna(dt, self.ambiente)
            if not lb.vivo:
                self.linfo_b.remove(lb)

        fattore_opsonizzazione = 1.0 + (self.ambiente.anticorpi / LIMITE_ANTICORPI) * 1.5

        nuovi_batteri: list[Batterio] = []
        for b in self.batteri:
            prob_morte = efficacia_antibiotico * 0.01 * fattore_opsonizzazione
            if prob_morte > 0 and random.random() < prob_morte * dt:
                b.vivo = False
                continue
            b.aggiorna(dt, self.ambiente)
            if b.pronto_duplicazione and len(self.batteri) < 200:
                nb = b.duplica()
                if nb:
                    nuovi_batteri.append(nb)
        self.batteri.extend(nuovi_batteri)
        self.batteri = [b for b in self.batteri if b.vivo]

        stats = self._raccogli_statistiche()
        stats["seed"] = self.seed
        self.logger.update(dt, stats)

    def run_until(self, durata: float) -> str:
        """Esegue la simulazione fino a 'durata' secondi simulati o estinzione batteri.

        Ritorna il percorso del CSV esportato.
        """
        dt = 1.0 / FPS  # usiamo lo stesso passo della versione interattiva
        while self.tempo_simulato < durata and self.batteri:
            self.step(dt)

        if self.logger.has_data():
            return self.logger.export_csv()
        return ""


def main() -> None:
    parser = argparse.ArgumentParser(
        description=f"ImmunoMind batch — {MARCHIO} ({AUTORE})"
    )
    parser.add_argument("--durata", type=float, default=3600.0, help="Durata simulazione (secondi simulati)")
    parser.add_argument("--repliche", type=int, default=5, help="Numero di repliche indipendenti")
    parser.add_argument(
        "--seed-base",
        type=int,
        default=None,
        help="Seed base per generare i seed delle repliche (se omesso usa RANDOM_SEED/valore casuale)",
    )
    args = parser.parse_args()

    print(f"ImmunoMind — modalità batch  ·  {MARCHIO}  ·  {AUTORE}")
    print(COPYRIGHT)
    print(f"Durata per run: {args.durata:.0f} s simulati, repliche: {args.repliche}")

    base = args.seed_base if args.seed_base is not None else RANDOM_SEED
    for i in range(args.repliche):
        seed = base + i if base is not None else None
        core = SimulationCore(seed=seed)
        print(f"\n▶ Run {i+1}/{args.repliche}  (seed={core.seed})...")
        path = core.run_until(args.durata)
        if path:
            print(f"   📊 CSV salvato in: {path}")
        else:
            print("   ℹ️ Nessun dato prodotto.")

    print("\n✅ Batch completato.")


if __name__ == "__main__":
    main()

