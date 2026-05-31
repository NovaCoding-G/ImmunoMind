"""Cellule e patogeni. © G.Roscino / NovaCoding."""

import pygame
import random
import math
from config import *


class Entita:
    """Base comune: posizione, colore, velocità e ciclo di vita."""
    
    def __init__(self, x, y, dimensione, colore, velocita):
        self.x = x
        self.y = y
        self.dimensione = dimensione
        self.colore = colore
        self.velocita = velocita
        self.vivo = True
        self.eta = 0  # Età in secondi simulati
        
        self.vx = random.uniform(-velocita, velocita)
        self.vy = random.uniform(-velocita, velocita)
    
    def aggiorna(self, dt, ambiente):
        """Aggiorna lo stato dell'entità (da sovrascrivere)"""
        self.eta += dt
        self.muovi(dt, ambiente)
    
    def muovi(self, dt, ambiente):
        """Movimento base con rimbalzo sui bordi"""
        self.x += self.vx * dt
        self.y += self.vy * dt
        
        if self.x < self.dimensione or self.x > AREA_SIMULAZIONE_X - self.dimensione:
            self.vx *= -1
            self.x = max(self.dimensione, min(self.x, AREA_SIMULAZIONE_X - self.dimensione))
        
        if self.y < self.dimensione or self.y > AREA_SIMULAZIONE_Y - self.dimensione:
            self.vy *= -1
            self.y = max(self.dimensione, min(self.y, AREA_SIMULAZIONE_Y - self.dimensione))
    
    def disegna(self, schermo):
        """Disegna l'entità sullo schermo"""
        pygame.draw.circle(schermo, self.colore, (int(self.x), int(self.y)), self.dimensione)
    
    def distanza_da(self, altra_entita):
        """Calcola la distanza euclidea da un'altra entità"""
        dx = self.x - altra_entita.x
        dy = self.y - altra_entita.y
        return math.sqrt(dx*dx + dy*dy)
    
    def collide_con(self, altra_entita):
        """Verifica se c'è collisione con un'altra entità"""
        distanza = self.distanza_da(altra_entita)
        return distanza < (self.dimensione + altra_entita.dimensione)


class GlobuloRosso(Entita):
    """Eritrocita - trasporta ossigeno nel flusso sanguigno"""
    
    def __init__(self, x, y):
        super().__init__(x, y, GLOBULO_ROSSO_DIMENSIONE, COLORE_GLOBULO_ROSSO, GLOBULO_ROSSO_VELOCITA)
        self.ossigeno = 100  # Percentuale saturazione
    
    def aggiorna(self, dt, ambiente):
        """I globuli rossi seguono principalmente il flusso sanguigno in modo continuo"""
        self.eta += dt
        
        self.vx = ambiente.flusso_x + random.uniform(-3, 3)
        self.vy = ambiente.flusso_y + random.uniform(-1.5, 1.5)
        
        self.x += self.vx * dt
        self.y += self.vy * dt
        
        limite_dx = AREA_SIMULAZIONE_X + self.dimensione * 2
        if self.x > limite_dx:
            self.x = -self.dimensione * 2
            self.y = random.randint(self.dimensione, AREA_SIMULAZIONE_Y - self.dimensione)
        
        if self.x < -self.dimensione * 3:
            self.x = random.randint(0, AREA_SIMULAZIONE_X // 4)
        
        if self.y < self.dimensione:
            self.y = self.dimensione
        elif self.y > AREA_SIMULAZIONE_Y - self.dimensione:
            self.y = AREA_SIMULAZIONE_Y - self.dimensione
    
    def disegna(self, schermo):
        """Disegna come disco biconcavo (due cerchi sovrapposti)"""
        pygame.draw.circle(schermo, self.colore, (int(self.x), int(self.y)), self.dimensione)
        colore_chiaro = tuple(min(c + 50, 255) for c in self.colore)
        pygame.draw.circle(schermo, colore_chiaro, (int(self.x), int(self.y)), self.dimensione - 2)


class Neutrofilo(Entita):
    """Neutrofilo - fagocita rapido, prima linea difesa"""
    
    def __init__(self, x, y):
        super().__init__(x, y, NEUTROFILO_DIMENSIONE, COLORE_NEUTROFILO, NEUTROFILO_VELOCITA)
        self.batteri_fagocitati = 0
        self.max_fagocitosi = NEUTROFILO_CAPACITA_FAGOCITOSI
        self.vita_max = NEUTROFILO_VITA
        self.stato = "pattuglia"  # pattuglia, inseguimento, fagocitosi
        self.target = None
        self.tempo_fagocitosi = 0
    
    def aggiorna(self, dt, ambiente):
        """Aggiorna comportamento del neutrofilo"""
        self.eta += dt
        
        if self.eta > self.vita_max:
            self.vivo = False
            return
        
        if self.batteri_fagocitati >= self.max_fagocitosi:
            self.vivo = False
            return
        
        if self.stato == "fagocitosi":
            self.tempo_fagocitosi += dt
            if self.tempo_fagocitosi >= NEUTROFILO_TEMPO_FAGOCITOSI:
                self.batteri_fagocitati += 1
                self.stato = "pattuglia"
                self.target = None
                self.tempo_fagocitosi = 0
        
        elif self.stato == "inseguimento" and self.target:
            if not self.target.vivo:
                self.stato = "pattuglia"
                self.target = None
            else:
                dx = self.target.x - self.x
                dy = self.target.y - self.y
                distanza = math.sqrt(dx*dx + dy*dy)
                
                if distanza < self.dimensione + self.target.dimensione:
                    if random.random() < NEUTROFILO_PROBABILITA_FAGOCITOSI:
                        self.stato = "fagocitosi"
                        self.target.vivo = False
                        self.tempo_fagocitosi = 0
                    else:
                        self.stato = "pattuglia"
                        self.target = None
                else:
                    self.vx = (dx / distanza) * self.velocita
                    self.vy = (dy / distanza) * self.velocita
        
        else:  # pattuglia
            if random.random() < 0.02:  # Cambia direzione occasionalmente
                angolo = random.uniform(0, 2 * math.pi)
                self.vx = math.cos(angolo) * self.velocita * 0.5
                self.vy = math.sin(angolo) * self.velocita * 0.5
        
        self.muovi(dt, ambiente)
    
    def rileva_patogeni(self, patogeni):
        """Cerca patogeni nel raggio di rilevamento"""
        if self.stato != "pattuglia":
            return
        
        for patogeno in patogeni:
            if not patogeno.vivo:
                continue
            
            distanza = self.distanza_da(patogeno)
            if distanza < NEUTROFILO_RAGGIO_RILEVAMENTO:
                self.target = patogeno
                self.stato = "inseguimento"
                break
    
    def disegna(self, schermo):
        """Disegna neutrofilo con nucleo multilobato"""
        pygame.draw.circle(schermo, self.colore, (int(self.x), int(self.y)), self.dimensione)
        
        colore_nucleo = (30, 80, 150)
        offset = 3
        pygame.draw.circle(schermo, colore_nucleo, (int(self.x - offset), int(self.y)), 3)
        pygame.draw.circle(schermo, colore_nucleo, (int(self.x + offset), int(self.y)), 3)
        pygame.draw.circle(schermo, colore_nucleo, (int(self.x), int(self.y + offset)), 3)
        
        if self.stato == "inseguimento":
            pygame.draw.circle(schermo, (255, 255, 0), (int(self.x), int(self.y)), 
                             self.dimensione + 3, 1)


class Batterio(Entita):
    """Batterio patogeno (E. coli)"""
    
    def __init__(self, x, y):
        super().__init__(x, y, BATTERIO_DIMENSIONE, COLORE_BATTERIO, BATTERIO_VELOCITA)
        self.tipo = "batterio"
        self.energia = BATTERIO_ENERGIA_INIZIALE
        self.tempo_duplicazione = 0
        self.pronto_duplicazione = False
    
    def aggiorna(self, dt, ambiente):
        """Aggiorna stato del batterio"""
        self.eta += dt
        self.tempo_duplicazione += dt
        
        self.energia -= dt * 0.1
        
        if self.energia <= 0:
            self.vivo = False
            return
        
        if self.tempo_duplicazione >= BATTERIO_TEMPO_DUPLICAZIONE:
            self.pronto_duplicazione = True
        
        if random.random() < 0.05:
            angolo = random.uniform(0, 2 * math.pi)
            self.vx = math.cos(angolo) * self.velocita
            self.vy = math.sin(angolo) * self.velocita
        
        self.muovi(dt, ambiente)
    
    def duplica(self):
        """Crea un nuovo batterio per divisione binaria"""
        if self.pronto_duplicazione:
            self.tempo_duplicazione = 0
            self.pronto_duplicazione = False
            nuovo_x = self.x + random.uniform(-10, 10)
            nuovo_y = self.y + random.uniform(-10, 10)
            return Batterio(nuovo_x, nuovo_y)
        return None
    
    def disegna(self, schermo):
        """Disegna batterio a forma di bastoncello"""
        rect = pygame.Rect(int(self.x - self.dimensione), 
                          int(self.y - self.dimensione//2),
                          self.dimensione * 2, 
                          self.dimensione)
        pygame.draw.ellipse(schermo, self.colore, rect)

        if random.random() < 0.3:
            pygame.draw.line(schermo, self.colore, 
                           (int(self.x - self.dimensione), int(self.y)),
                           (int(self.x - self.dimensione - 5), int(self.y + random.randint(-3, 3))), 1)


class Virus(Entita):
    """Virus patogeno (modello semplificato come particelle extracellulari)"""
    
    def __init__(self, x, y):
        super().__init__(x, y, VIRUS_DIMENSIONE, COLORE_VIRUS, VIRUS_VELOCITA)
        self.tipo = "virus"
        self.energia = VIRUS_ENERGIA_INIZIALE
        self.tempo_duplicazione = 0
        self.pronto_duplicazione = False
    
    def aggiorna(self, dt, ambiente):
        self.eta += dt
        self.tempo_duplicazione += dt
        
        self.energia -= dt * 0.12
        if self.energia <= 0:
            self.vivo = False
            return
        
        if self.tempo_duplicazione >= VIRUS_TEMPO_DUPLICAZIONE:
            self.pronto_duplicazione = True
        
        if random.random() < 0.06:
            angolo = random.uniform(0, 2 * math.pi)
            self.vx = math.cos(angolo) * self.velocita
            self.vy = math.sin(angolo) * self.velocita
        
        self.muovi(dt, ambiente)
    
    def duplica(self):
        if self.pronto_duplicazione:
            self.tempo_duplicazione = 0
            self.pronto_duplicazione = False
            nuovo_x = self.x + random.uniform(-10, 10)
            nuovo_y = self.y + random.uniform(-10, 10)
            return Virus(nuovo_x, nuovo_y)
        return None
    
    def disegna(self, schermo):
        pygame.draw.circle(schermo, self.colore, (int(self.x), int(self.y)), self.dimensione)
        pygame.draw.circle(
            schermo,
            (255, 185, 110),
            (int(self.x), int(self.y)),
            max(2, self.dimensione - 1),
            1,
        )


class Macrofago(Entita):
    """Macrofago - fagocita potente, rilascia più citochine"""
    
    def __init__(self, x, y):
        super().__init__(x, y, MACROFAGO_DIMENSIONE, COLORE_MACROFAGO, MACROFAGO_VELOCITA)
        self.batteri_fagocitati = 0
        self.virus_fagocitati = 0
        self.max_fagocitosi = MACROFAGO_CAPACITA_FAGOCITOSI
        self.vita_max = MACROFAGO_VITA
        self.target = None
        self.target_tipo = None
        self.stato = "pattuglia"  # pattuglia, inseguimento, fagocitosi
        self.tempo_fagocitosi = 0
    
    def aggiorna(self, dt, ambiente):
        self.eta += dt
        if self.eta > self.vita_max or (self.batteri_fagocitati + self.virus_fagocitati) >= self.max_fagocitosi:
            self.vivo = False
            return
        
        if self.stato == "fagocitosi":
            self.tempo_fagocitosi += dt
            if self.tempo_fagocitosi >= NEUTROFILO_TEMPO_FAGOCITOSI * 1.2:
                if self.target_tipo == "virus":
                    self.virus_fagocitati += 1
                else:
                    self.batteri_fagocitati += 1
                self.stato = "pattuglia"
                self.target = None
                self.target_tipo = None
                self.tempo_fagocitosi = 0
                ambiente.aggiungi_citochine(self.x, self.y, 40)
        elif self.stato == "inseguimento" and self.target:
            if not self.target.vivo:
                self.stato = "pattuglia"
                self.target = None
            else:
                dx = self.target.x - self.x
                dy = self.target.y - self.y
                distanza = math.sqrt(dx * dx + dy * dy)
                if distanza < self.dimensione + self.target.dimensione:
                    if random.random() < MACROFAGO_PROBABILITA_FAGOCITOSI:
                        self.stato = "fagocitosi"
                        self.target_tipo = getattr(self.target, "tipo", None)
                        self.target.vivo = False
                        self.tempo_fagocitosi = 0
                    else:
                        self.stato = "pattuglia"
                        self.target = None
                        self.target_tipo = None
                else:
                    self.vx = (dx / distanza) * self.velocita
                    self.vy = (dy / distanza) * self.velocita
        else:
            if random.random() < 0.015:
                angolo = random.uniform(0, 2 * math.pi)
                self.vx = math.cos(angolo) * self.velocita * 0.4
                self.vy = math.sin(angolo) * self.velocita * 0.4
        
        self.muovi(dt, ambiente)
    
    def rileva_patogeni(self, patogeni):
        if self.stato != "pattuglia":
            return
        for p in patogeni:
            if not p.vivo:
                continue
            if self.distanza_da(p) < MACROFAGO_RAGGIO_RILEVAMENTO:
                self.target = p
                self.stato = "inseguimento"
                break
    
    def disegna(self, schermo):
        pygame.draw.circle(schermo, self.colore, (int(self.x), int(self.y)), self.dimensione)
        for _ in range(4):
            rx = random.randint(-self.dimensione + 1, self.dimensione - 1)
            ry = random.randint(-self.dimensione + 1, self.dimensione - 1)
            pygame.draw.circle(
                schermo,
                (80, 140, 80),
                (int(self.x + rx * 0.4), int(self.y + ry * 0.4)),
                2,
            )


class LinfocitaT(Entita):
    """Linfocita T citotossico - potenzia l'eliminazione localizzata dei patogeni"""
    
    def __init__(self, x, y):
        super().__init__(x, y, LINFO_T_DIMENSIONE, COLORE_LINFOCITA_T, LINFO_T_VELOCITA)
        self.vita_max = LINFO_T_VITA
    
    def aggiorna(self, dt, ambiente, patogeni):
        self.eta += dt
        if self.eta > self.vita_max:
            self.vivo = False
            return
        
        self._drift_citochine(dt, ambiente)
        self.muovi(dt, ambiente)
        
        for p in patogeni:
            if not p.vivo:
                continue
            if self.distanza_da(p) < LINFO_T_RAGGIO_AZIONE:
                prob_base = LINFO_T_PROB_UCCISIONE
                if getattr(p, "tipo", None) == "virus":
                    prob = prob_base * 1.3
                else:
                    prob = prob_base * 0.4
                if random.random() < prob * dt:
                    p.vivo = False
    
    def _drift_citochine(self, dt, ambiente):
        cx, cy = AREA_SIMULAZIONE_X / 2, AREA_SIMULAZIONE_Y / 2
        dx, dy = cx - self.x, cy - self.y
        distanza = math.hypot(dx, dy)
        if distanza > 0:
            self.vx += (dx / distanza) * self.velocita * 0.1 * dt
            self.vy += (dy / distanza) * self.velocita * 0.1 * dt
    
    def disegna(self, schermo):
        pygame.draw.circle(schermo, self.colore, (int(self.x), int(self.y)), self.dimensione)
        pygame.draw.circle(
            schermo,
            (230, 200, 255),
            (int(self.x), int(self.y)),
            self.dimensione + 1,
            1,
        )


class LinfocitaB(Entita):
    """Linfocita B - sorgente di anticorpi (effetto globale)"""
    
    def __init__(self, x, y):
        super().__init__(x, y, LINFO_B_DIMENSIONE, COLORE_LINFOCITA_B, LINFO_B_VELOCITA)
        self.vita_max = LINFO_B_VITA
    
    def aggiorna(self, dt, ambiente):
        self.eta += dt
        if self.eta > self.vita_max:
            self.vivo = False
            return
        
        if random.random() < 0.02:
            angolo = random.uniform(0, 2 * math.pi)
            self.vx = math.cos(angolo) * self.velocita * 0.3
            self.vy = math.sin(angolo) * self.velocita * 0.3
        
        self.muovi(dt, ambiente)
        
        ambiente.anticorpi = min(
            LIMITE_ANTICORPI,
            ambiente.anticorpi + LINFO_B_TASSO_ANTICORPI * dt,
        )
    
    def disegna(self, schermo):
        pygame.draw.circle(schermo, self.colore, (int(self.x), int(self.y)), self.dimensione)
        pygame.draw.circle(
            schermo,
            COLORE_ANTICORPO,
            (int(self.x), int(self.y)),
            self.dimensione + 2,
            1,
        )

