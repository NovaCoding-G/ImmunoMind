"""Ambiente vascolare e farmaci. © G.Roscino / NovaCoding."""

import pygame
import random
import math
from config import *


class Ambiente:
    """Il mondo in cui vivono cellule e patogeni: caldo, ossigeno, flusso."""
    
    def __init__(self):
        self.temperatura = TEMPERATURA_NORMALE
        self.ossigeno = CONCENTRAZIONE_OSSIGENO_NORMALE
        self.nutrienti = CONCENTRAZIONE_NUTRIENTI_NORMALE
        self.anticorpi = 0.0
        
        self.flusso_x = 15  # pixel/frame verso destra
        self.flusso_y = 0   # flusso orizzontale
        
        self.griglia_citochine = [[0 for _ in range(30)] for _ in range(30)]
        
        self.particelle_flusso = []
        for _ in range(50):
            self.particelle_flusso.append({
                'x': random.randint(0, AREA_SIMULAZIONE_X),
                'y': random.randint(0, AREA_SIMULAZIONE_Y),
                'velocita': random.uniform(10, 20)
            })
    
    def aggiorna(self, dt, num_patogeni):
        """Aggiorna lo stato dell'ambiente"""
        
        if num_patogeni > 10:
            self.temperatura = min(self.temperatura + dt * 0.01, TEMPERATURA_FEBBRE)
        else:
            self.temperatura = max(self.temperatura - dt * 0.005, TEMPERATURA_NORMALE)
        
        for p in self.particelle_flusso:
            p['x'] += self.flusso_x * dt
            if p['x'] > AREA_SIMULAZIONE_X:
                p['x'] = 0
                p['y'] = random.randint(0, AREA_SIMULAZIONE_Y)
    
    def aggiungi_citochine(self, x, y, intensita):
        """Aggiunge citochine infiammatorie in una posizione"""
        grid_x = int(x / AREA_SIMULAZIONE_X * 30)
        grid_y = int(y / AREA_SIMULAZIONE_Y * 30)
        
        if 0 <= grid_x < 30 and 0 <= grid_y < 30:
            self.griglia_citochine[grid_y][grid_x] = min(
                self.griglia_citochine[grid_y][grid_x] + intensita, 255
            )
    
    def dissipa_citochine(self, dt):
        """Dissipa gradualmente le citochine"""
        for y in range(30):
            for x in range(30):
                self.griglia_citochine[y][x] *= 0.99  # Decade lentamente
    
    def disegna_sfondo(self, schermo):
        """Disegna lo sfondo con effetto flusso sanguigno"""
        schermo.fill(COLORE_SFONDO)
        
        for p in self.particelle_flusso:
            pygame.draw.circle(schermo, COLORE_PARTICELLA_FLUSSO, 
                             (int(p['x']), int(p['y'])), 2)
    
    def disegna_heatmap_citochine(self, schermo):
        """Disegna mappa di calore delle citochine (opzionale)"""
        cell_width = AREA_SIMULAZIONE_X // 30
        cell_height = AREA_SIMULAZIONE_Y // 30
        
        superficie = pygame.Surface((AREA_SIMULAZIONE_X, AREA_SIMULAZIONE_Y), pygame.SRCALPHA)
        
        for y in range(30):
            for x in range(30):
                intensita = int(self.griglia_citochine[y][x])
                if intensita > 0:
                    r, g, b, _ = COLORE_CITOCHINA
                    colore = (r, g, b, min(intensita, 100))
                    rect = pygame.Rect(x * cell_width, y * cell_height, 
                                      cell_width, cell_height)
                    pygame.draw.rect(superficie, colore, rect)
        
        schermo.blit(superficie, (0, 0))


class GestoreFarmaci:
    """Somministrazione farmaci, emivita e efficacia nel tempo."""
    
    def __init__(self):
        self.farmaci_attivi = []
    
    def aggiungi_farmaco(self, tipo, dose):
        """Aggiunge un farmaco al sistema"""
        farmaco = {
            'tipo': tipo,
            'concentrazione': dose,
            'tempo_somministrazione': 0
        }
        self.farmaci_attivi.append(farmaco)
    
    def aggiorna(self, dt):
        """Aggiorna concentrazione farmaci (emivita)"""
        farmaci_da_rimuovere = []
        
        for farmaco in self.farmaci_attivi:
            farmaco['tempo_somministrazione'] += dt
            
            if farmaco['tipo'] == 'penicillina':
                emivita = PENICILLINA_EMIVITA
                farmaco['concentrazione'] *= math.exp(-0.693 * dt / emivita)
            elif farmaco['tipo'] == 'oseltamivir':
                emivita = OSELTAMIVIR_EMIVITA
                farmaco['concentrazione'] *= math.exp(-0.693 * dt / emivita)
            elif farmaco['tipo'] == 'aciclovir':
                emivita = ACICLOVIR_EMIVITA
                farmaco['concentrazione'] *= math.exp(-0.693 * dt / emivita)
            
            if farmaco['concentrazione'] < 1:
                farmaci_da_rimuovere.append(farmaco)
        
        for farmaco in farmaci_da_rimuovere:
            self.farmaci_attivi.remove(farmaco)
    
    def ottieni_efficacia_antibiotico(self):
        """Calcola efficacia totale antibiotica"""
        efficacia_totale = 0
        for farmaco in self.farmaci_attivi:
            if farmaco['tipo'] == 'penicillina':
                efficacia_totale += (farmaco['concentrazione'] / PENICILLINA_DOSE_STANDARD) * PENICILLINA_EFFICACIA
        
        return min(efficacia_totale, 1.0)  # Max 100%

    def ottieni_efficacia_antivirale(self):
        """Calcola efficacia totale antivirale (oseltamivir + aciclovir)."""
        efficacia_totale = 0.0
        for farmaco in self.farmaci_attivi:
            if farmaco["tipo"] == "oseltamivir":
                efficacia_totale += (
                    (farmaco["concentrazione"] / OSELTAMIVIR_DOSE_STANDARD) * OSELTAMIVIR_EFFICACIA
                )
            elif farmaco["tipo"] == "aciclovir":
                efficacia_totale += (
                    (farmaco["concentrazione"] / ACICLOVIR_DOSE_STANDARD) * ACICLOVIR_EFFICACIA
                )
        return min(efficacia_totale, 1.0)
    
    def ottieni_concentrazione_totale(self, tipo):
        """Ottiene concentrazione totale di un tipo di farmaco"""
        concentrazione = 0
        for farmaco in self.farmaci_attivi:
            if farmaco['tipo'] == tipo:
                concentrazione += farmaco['concentrazione']
        return concentrazione

