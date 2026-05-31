"""Loop principale, UI e simulazione. © G.Roscino / NovaCoding."""

import pygame
import sys
import random

from brand import (
    MARCHIO,
    AUTORE,
    PROGETTO,
    VERSIONE,
    COPYRIGHT,
    riga_avvio_console,
    crediti_brevi,
)
from config import *
from fonts import ui_font, brand_title_font, subtitle_font, section_font, label_font, body_font, caption_font
from entita_base import (
    GlobuloRosso,
    Neutrofilo,
    Batterio,
    Virus,
    Macrofago,
    LinfocitaT,
    LinfocitaB,
)
from ambiente import Ambiente, GestoreFarmaci
from hud import HUD
from analytics import SimulationLogger
from WIKI import WIKI_SECTIONS


# Console Windows: evita crash con caratteri Unicode (cp1252).
try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


class ImmunoMind:
    """Simulatore: input → aggiornamento → disegno ogni frame."""

    def __init__(self):
        pygame.init()
        self.fullscreen = FULLSCREEN
        flags = pygame.FULLSCREEN if self.fullscreen else 0
        self.schermo = pygame.display.set_mode((LARGHEZZA, ALTEZZA), flags)
        pygame.display.set_caption(TITOLO)
        self.clock = pygame.time.Clock()

        self.ambiente = Ambiente()
        self.gestore_farmaci = GestoreFarmaci()
        self.hud = HUD()

        if RANDOM_SEED is not None:
            self.seed = RANDOM_SEED
        else:
            self.seed = int(pygame.time.get_ticks())
        random.seed(self.seed)

        self.globuli_rossi = []
        self.neutrofili = []
        self.macrofagi = []
        self.linfo_t = []
        self.linfo_b = []
        self.batteri = []
        self.virus = []

        self.scenario_attivo = "batterica"
        self.gravita = 2
        self.tutorial_attivo = False
        self.tutorial_start_ms = 0
        self.tutorial_step = 0
        self.tutorial_testi = []

        self.in_esecuzione = True
        self.in_pausa = False
        self.velocita_simulazione = 1
        self.tempo_simulato = 0
        self.batteri_fagocitati_totali = 0

        self.logger = SimulationLogger(run_id=str(self.seed), enabled=True)

        self._inizializza_popolazione()

        self.ui_screen = "home"
        self._ui_last_screen = "home"
        self.mostra_menu = True
        self._ui_buttons = {}
        self._sim_ha_avviato_almeno_una_volta = False

        self._wiki_open = set()
        self._wiki_scroll = 0
        self._wiki_scroll_max = 0
        self._wiki_hitboxes = []

    def _ui_make_button(self, key, rect, label, kind="primary"):
        self._ui_buttons[key] = {"rect": rect, "label": label, "kind": kind}

    def _ui_hit(self, key, pos):
        btn = self._ui_buttons.get(key)
        return bool(btn and btn["rect"].collidepoint(pos))

    def _ui_draw_button(self, key, font, mouse_pos):
        btn = self._ui_buttons[key]
        rect = btn["rect"]
        label = btn["label"]
        kind = btn["kind"]

        hovered = rect.collidepoint(mouse_pos)

        if kind == "nav":
            bg = COLORE_UI_BTN_NAV_BG_HOVER if hovered else COLORE_UI_BTN_NAV_BG
            fg = COLORE_UI_BTN_NAV_FG
            border = COLORE_UI_BTN_NAV_BORDER
        elif kind == "secondary":
            bg = COLORE_UI_BTN_SEC_BG_HOVER if hovered else COLORE_UI_BTN_SEC_BG
            fg = COLORE_UI_BTN_SEC_FG
            border = COLORE_UI_BTN_SEC_BORDER
        else:  # primary
            bg = COLORE_UI_BTN_PRI_BG_HOVER if hovered else COLORE_UI_BTN_PRI_BG
            fg = COLORE_UI_BTN_PRI_FG
            border = COLORE_UI_BTN_PRI_BORDER

        pygame.draw.rect(self.schermo, bg, rect, border_radius=10)
        pygame.draw.rect(self.schermo, border, rect, width=2, border_radius=10)

        t = font.render(label, True, fg)
        tr = t.get_rect(center=rect.center)
        self.schermo.blit(t, tr)
    
    def _ui_blit_text_shadow(self, text_surf, x, y, shadow=(0, 0, 0), shadow_alpha=120, offset=(2, 2)):
        """Disegna testo con ombra leggera (leggibilità su sfondi scuri)."""
        if text_surf is None:
            return
        sh = text_surf.copy()
        sh.fill((*shadow, shadow_alpha), special_flags=pygame.BLEND_RGBA_MULT)
        self.schermo.blit(sh, (x + offset[0], y + offset[1]))
        self.schermo.blit(text_surf, (x, y))

    def _ui_draw_page_title(self, text, x, y, font_size=None):
        """Titolo pagina secondaria (Scenari, Gravità, Wiki, Informazioni): compatto, in rettangolo arrotondato."""
        if font_size is None:
            font_size = FONT_UI_PAGE_TITLE
        pad_x, pad_y = 12, 7
        f = ui_font(font_size, bold=True)
        surf = f.render(text, True, COLORE_TIPO_TITOLO)
        w = max(200, surf.get_width() + pad_x * 2)
        h = max(30, surf.get_height() + pad_y * 2)
        r = pygame.Rect(int(x), int(y), w, h)
        panel = pygame.Surface((w, h), pygame.SRCALPHA)
        panel.fill(COLORE_UI_PAGINA_TITOLO_BG)
        self.schermo.blit(panel, r.topleft)
        pygame.draw.rect(self.schermo, COLORE_UI_PAGINA_TITOLO_BORDO, r, width=1, border_radius=8)
        tx = r.x + pad_x
        ty = r.y + (h - surf.get_height()) // 2
        self._ui_blit_text_shadow(surf, tx, ty, shadow_alpha=95, offset=(1, 1))
        return r.bottom

    def _ui_draw_typo_line(self, kind, text, x, y, fonts):
        """Disegna una riga con gerarchia tipografica (titolo / sezione / corpo / caption)."""
        if kind == "blank" or not text:
            return y + 10
        font_map = {
            "title": (fonts["title"], COLORE_TIPO_TITOLO),
            "section": (fonts["section"], COLORE_TIPO_SEZIONE),
            "body": (fonts["body"], COLORE_TIPO_CORPO),
            "caption": (fonts["caption"], COLORE_TIPO_MUTED),
        }
        font, color = font_map.get(kind, (fonts["body"], COLORE_TIPO_CORPO))
        surf = font.render(text, True, color)
        self._ui_blit_text_shadow(surf, x, y, shadow_alpha=90, offset=(2, 2))
        return y + surf.get_height() + 10

    def _wiki_blit_line_colored(self, line, x, y, font_body, font_label):
        """Riga Wiki: prefissi entità con gli stessi colori del simulatore / HUD."""
        wiki_entity_prefixes = (
            ("Linfociti T:", COLORE_LINFOCITA_T),
            ("Linfociti B:", COLORE_LINFOCITA_B),
            ("Globuli rossi:", COLORE_GLOBULO_ROSSO),
            ("Neutrofili:", COLORE_NEUTROFILO),
            ("Macrofagi:", COLORE_MACROFAGO),
            ("Batteri e virus:", COLORE_BATTERIO),
        )
        rest_color = COLORE_TIPO_CORPO
        for pref, col in wiki_entity_prefixes:
            if line.startswith(pref):
                cx = x
                s1 = font_label.render(pref, True, col)
                self._ui_blit_text_shadow(s1, cx, y, shadow_alpha=95, offset=(2, 2))
                cx += s1.get_width()
                tail = line[len(pref) :]
                s2 = font_body.render(tail, True, rest_color)
                self._ui_blit_text_shadow(s2, cx, y, shadow_alpha=95, offset=(2, 2))
                return
        s = font_body.render(line, True, COLORE_TIPO_CORPO)
        self._ui_blit_text_shadow(s, x, y, shadow_alpha=95, offset=(2, 2))

    def _ui_set_screen(self, screen):
        if self.ui_screen == "sim" and screen != "sim":
            self.tutorial_attivo = False
        self._ui_last_screen = self.ui_screen
        self.ui_screen = screen
        self.mostra_menu = (self.ui_screen != "sim")
        if self.ui_screen != "wiki":
            self._wiki_scroll = 0
    
    def _inizializza_popolazione(self):
        """Crea la popolazione iniziale di cellule e patogeni"""
        
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
        
        self._spawn_patogeni_iniziali()

    def _spawn_patogeni_iniziali(self):
        """Crea i patogeni iniziali in base allo scenario attivo."""
        self.batteri.clear()
        self.virus.clear()
        
        if self.scenario_attivo == "batterica":
            num = int(NUM_BATTERI_INIZIALE * self.gravita)
            for _ in range(num):
                x = random.randint(100, AREA_SIMULAZIONE_X - 100)
                y = random.randint(100, AREA_SIMULAZIONE_Y - 100)
                self.batteri.append(Batterio(x, y))
            self.ambiente.temperatura = TEMPERATURA_NORMALE
            self.ambiente.anticorpi = 0.0
            self.tempo_attivazione_adattativa_attuale = TEMPO_ATTIVAZIONE_ADATTATIVA
        
        elif self.scenario_attivo == "virale":
            num_v = int(8 * self.gravita)
            for _ in range(num_v):
                x = random.randint(100, AREA_SIMULAZIONE_X - 100)
                y = random.randint(100, AREA_SIMULAZIONE_Y - 100)
                self.virus.append(Virus(x, y))
            self.ambiente.temperatura = TEMPERATURA_NORMALE
            self.ambiente.anticorpi = 0.0
            self.tempo_attivazione_adattativa_attuale = TEMPO_ATTIVAZIONE_ADATTATIVA
            self.ambiente.aggiungi_citochine(AREA_SIMULAZIONE_X // 2, AREA_SIMULAZIONE_Y // 2, 60)
        
        elif self.scenario_attivo == "vaccino":
            num = max(3, int(NUM_BATTERI_INIZIALE * 0.6 * self.gravita))
            for _ in range(num):
                x = random.randint(120, AREA_SIMULAZIONE_X - 120)
                y = random.randint(120, AREA_SIMULAZIONE_Y - 200)
                self.batteri.append(Batterio(x, y))
            
            self.ambiente.anticorpi = LIMITE_ANTICORPI * 0.6
            self.ambiente.temperatura = TEMPERATURA_NORMALE
            self.tempo_attivazione_adattativa_attuale = int(TEMPO_ATTIVAZIONE_ADATTATIVA * 0.15)
            
            self.linfo_b.clear()
            self.linfo_t.clear()
            for _ in range(4):
                x = random.randint(50, AREA_SIMULAZIONE_X - 50)
                y = random.randint(50, AREA_SIMULAZIONE_Y - 50)
                self.linfo_b.append(LinfocitaB(x, y))
        
        elif self.scenario_attivo == "ferita":
            num = max(4, int(NUM_BATTERI_INIZIALE * 0.8 * self.gravita))
            for _ in range(num):
                x = random.randint(120, AREA_SIMULAZIONE_X - 120)
                y = random.randint(120, AREA_SIMULAZIONE_Y - 120)
                self.batteri.append(Batterio(x, y))
            
            self.ambiente.temperatura = TEMPERATURA_NORMALE + 0.4
            self.ambiente.anticorpi = 0.0
            self.tempo_attivazione_adattativa_attuale = int(TEMPO_ATTIVAZIONE_ADATTATIVA * 0.8)
            self.ambiente.aggiungi_citochine(
                AREA_SIMULAZIONE_X // 2,
                AREA_SIMULAZIONE_Y // 2 + 100,
                90,
            )
        
        else:
            num = int(NUM_BATTERI_INIZIALE * self.gravita)
            for _ in range(num):
                x = random.randint(100, AREA_SIMULAZIONE_X - 100)
                y = random.randint(100, AREA_SIMULAZIONE_Y - 100)
                self.batteri.append(Batterio(x, y))
            self.ambiente.temperatura = TEMPERATURA_NORMALE
            self.ambiente.anticorpi = 0.0
            self.tempo_attivazione_adattativa_attuale = TEMPO_ATTIVAZIONE_ADATTATIVA
    
    def gestisci_input(self):
        """Gestisce input da tastiera e mouse"""
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.in_esecuzione = False
            
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    if self.ui_screen == "sim":
                        self._ui_set_screen("home")
                        continue
                    else:
                        self._ui_set_screen("home")
                        continue
                
                elif evento.key == pygame.K_SPACE:
                    self.in_pausa = not self.in_pausa
                
                elif evento.key == pygame.K_1:
                    self.gestore_farmaci.aggiungi_farmaco('penicillina', PENICILLINA_DOSE_STANDARD)
                    print("Penicillina somministrata (100 mg/L)")

                elif evento.key == pygame.K_2:
                    self.gestore_farmaci.aggiungi_farmaco('oseltamivir', OSELTAMIVIR_DOSE_STANDARD)
                    print("Oseltamivir somministrato (100 mg/L)")

                elif evento.key == pygame.K_3:
                    self.gestore_farmaci.aggiungi_farmaco('aciclovir', ACICLOVIR_DOSE_STANDARD)
                    print("Aciclovir somministrato (100 mg/L)")
                
                elif evento.key == pygame.K_PLUS or evento.key == pygame.K_EQUALS:
                    if self.velocita_simulazione < 60:
                        self.velocita_simulazione *= 2
                        print(f"Velocità: {self.velocita_simulazione}x")
                
                elif evento.key == pygame.K_MINUS:
                    if self.velocita_simulazione > 1:
                        self.velocita_simulazione //= 2
                        print(f"Velocità: {self.velocita_simulazione}x")
                
                elif evento.key == pygame.K_r:
                    self._reset_simulazione()
                
                elif evento.key == pygame.K_n:
                    for _ in range(5):
                        x = random.randint(50, AREA_SIMULAZIONE_X - 50)
                        y = random.randint(50, AREA_SIMULAZIONE_Y - 50)
                        self.neutrofili.append(Neutrofilo(x, y))
                    print("+5 Neutrofili aggiunti")

                elif evento.key == pygame.K_f:
                    self.fullscreen = not self.fullscreen
                    flags = pygame.FULLSCREEN if self.fullscreen else 0
                    self.schermo = pygame.display.set_mode((LARGHEZZA, ALTEZZA), flags)
                    pygame.display.set_caption(TITOLO)

                elif evento.key == pygame.K_e:
                    if self.logger and self.logger.has_data():
                        path = self.logger.export_csv()
                        print(f"Dati esportati in: {path}")
                    else:
                        print("Nessun dato da esportare (lascia girare la simulazione qualche minuto).")
            
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    if self.ui_screen != "sim":
                        self._gestisci_click_ui((mouse_x, mouse_y))
                        continue
                    
                    if mouse_x < AREA_SIMULAZIONE_X and mouse_y < AREA_SIMULAZIONE_Y:
                        if self.scenario_attivo == "virale":
                            for _ in range(3):
                                offset_x = random.randint(-20, 20)
                                offset_y = random.randint(-20, 20)
                                self.virus.append(Virus(mouse_x + offset_x, mouse_y + offset_y))
                        else:
                            for _ in range(3):
                                offset_x = random.randint(-20, 20)
                                offset_y = random.randint(-20, 20)
                                self.batteri.append(Batterio(mouse_x + offset_x, mouse_y + offset_y))
                        self.ambiente.aggiungi_citochine(mouse_x, mouse_y, 50)
                    elif mouse_x >= AREA_SIMULAZIONE_X:
                        self.hud.handle_click((mouse_x, mouse_y))
            
            elif evento.type == pygame.MOUSEWHEEL:
                if self.ui_screen == "wiki":
                    self._wiki_scroll = max(0, min(self._wiki_scroll_max, self._wiki_scroll - evento.y * 28))

    def _gestisci_click_ui(self, pos):
        if self._ui_hit("nav_scenari", pos):
            self._ui_set_screen("scenari")
            return
        if self._ui_hit("nav_gravita", pos):
            self._ui_set_screen("gravita")
            return
        if self._ui_hit("nav_wiki", pos):
            self._ui_set_screen("wiki")
            return
        if self._ui_hit("nav_info", pos):
            self._ui_set_screen("info")
            return

        if self.ui_screen == "home":
            if self._ui_hit("start", pos):
                self._avvia_simulazione_da_ui()
                return
            if self._ui_hit("resume", pos):
                self._riprendi_simulazione_da_ui()
                return

        elif self.ui_screen == "scenari":
            if self._ui_hit("back", pos):
                self._ui_set_screen("home")
                return
            if self._ui_hit("sc_batterica", pos):
                self.scenario_attivo = "batterica"
                return
            if self._ui_hit("sc_virale", pos):
                self.scenario_attivo = "virale"
                return
            if self._ui_hit("sc_vaccino", pos):
                self.scenario_attivo = "vaccino"
                return
            if self._ui_hit("sc_ferita", pos):
                self.scenario_attivo = "ferita"
                return
            if self._ui_hit("start_from_scenari", pos):
                self._avvia_simulazione_da_ui()
                return

        elif self.ui_screen == "gravita":
            if self._ui_hit("back", pos):
                self._ui_set_screen("home")
                return
            if self._ui_hit("grav_minus", pos):
                self.gravita = max(1, self.gravita - 1)
                return
            if self._ui_hit("grav_plus", pos):
                self.gravita = min(5, self.gravita + 1)
                return
            for g in range(1, 6):
                if self._ui_hit(f"grav_{g}", pos):
                    self.gravita = g
                    return
            if self._ui_hit("start_from_gravita", pos):
                self._avvia_simulazione_da_ui()
                return

        elif self.ui_screen in ("wiki", "info"):
            if self.ui_screen == "wiki":
                for rect, idx in self._wiki_hitboxes:
                    if rect.collidepoint(pos):
                        if idx in self._wiki_open:
                            self._wiki_open.remove(idx)
                            action = "close"
                        else:
                            self._wiki_open.add(idx)
                            action = "open"
                        return
            if self._ui_hit("back", pos):
                self._ui_set_screen("home")
                return

    def _avvia_simulazione_da_ui(self):
        """Avvia la simulazione usando scenario + gravità selezionati."""
        self.in_pausa = False
        self._reset_simulazione()
        self._avvia_tutorial()
        self._sim_ha_avviato_almeno_una_volta = True
        self._ui_set_screen("sim")
    
    def _riprendi_simulazione_da_ui(self):
        """Ritorna alla simulazione senza resettare."""
        if not self._sim_ha_avviato_almeno_una_volta:
            return
        self.in_pausa = False
        self._ui_set_screen("sim")
    
    def _reset_simulazione(self):
        """Resetta la simulazione allo stato iniziale"""
        self.globuli_rossi.clear()
        self.neutrofili.clear()
        self.macrofagi.clear()
        self.linfo_t.clear()
        self.linfo_b.clear()
        self.batteri.clear()
        self.virus.clear()
        self.tutorial_attivo = False
        self.gestore_farmaci.farmaci_attivi.clear()
        self.tempo_simulato = 0
        self.batteri_fagocitati_totali = 0
        self._inizializza_popolazione()
        if self.logger:
            self.logger._records.clear()
        print("Simulazione resettata")
    
    def aggiorna(self, dt):
        """Aggiorna la simulazione"""
        
        if self.in_pausa or self.ui_screen != "sim":
            return
        
        dt_effettivo = dt * self.velocita_simulazione
        self.tempo_simulato += dt_effettivo
        
        patogeni_totali = len(self.batteri) + len(self.virus)
        self.ambiente.aggiorna(dt_effettivo, patogeni_totali)
        self.ambiente.dissipa_citochine(dt_effettivo)
        
        self.gestore_farmaci.aggiorna(dt_effettivo)
        efficacia_antibiotico = self.gestore_farmaci.ottieni_efficacia_antibiotico()
        efficacia_antivirale = self.gestore_farmaci.ottieni_efficacia_antivirale()
        
        for globulo in self.globuli_rossi:
            globulo.aggiorna(dt_effettivo, self.ambiente)
        
        for neutrofilo in self.neutrofili:
            neutrofilo.rileva_patogeni(self.batteri)
            neutrofilo.aggiorna(dt_effettivo, self.ambiente)
        
        neutrofili_morti = [n for n in self.neutrofili if not n.vivo]
        for neutrofilo in neutrofili_morti:
            self.batteri_fagocitati_totali += neutrofilo.batteri_fagocitati
            self.neutrofili.remove(neutrofilo)
        
        for macro in self.macrofagi:
            macro.rileva_patogeni(self.batteri + self.virus)
            macro.aggiorna(dt_effettivo, self.ambiente)
        self.macrofagi = [m for m in self.macrofagi if m.vivo]
        
        if self.tempo_simulato > self.tempo_attivazione_adattativa_attuale and patogeni_totali > 0:
            if len(self.linfo_t) < 10 and random.random() < 0.01:
                x = random.randint(50, AREA_SIMULAZIONE_X - 50)
                y = random.randint(50, AREA_SIMULAZIONE_Y - 50)
                self.linfo_t.append(LinfocitaT(x, y))
            if len(self.linfo_b) < 8 and random.random() < 0.008:
                x = random.randint(50, AREA_SIMULAZIONE_X - 50)
                y = random.randint(50, AREA_SIMULAZIONE_Y - 50)
                self.linfo_b.append(LinfocitaB(x, y))
        
        for lt in list(self.linfo_t):
            lt.aggiorna(dt_effettivo, self.ambiente, self.batteri + self.virus)
            if not lt.vivo:
                self.linfo_t.remove(lt)
        
        for lb in list(self.linfo_b):
            lb.aggiorna(dt_effettivo, self.ambiente)
            if not lb.vivo:
                self.linfo_b.remove(lb)
        
        fattore_opsonizzazione = 1.0 + (self.ambiente.anticorpi / LIMITE_ANTICORPI) * 1.5
        fattore_opsonizzazione_virus = 1.0 + (self.ambiente.anticorpi / LIMITE_ANTICORPI) * 1.0
        
        nuovi_batteri = []
        
        for batterio in self.batteri:
            if not batterio.vivo:
                continue
            prob_morte = efficacia_antibiotico * 0.01
            prob_morte *= fattore_opsonizzazione
            if prob_morte > 0 and random.random() < prob_morte * dt_effettivo:
                batterio.vivo = False
                continue
            
            batterio.aggiorna(dt_effettivo, self.ambiente)
            
            if batterio.pronto_duplicazione and len(self.batteri) < 200:  # Limite popolazione
                nuovo = batterio.duplica()
                if nuovo:
                    nuovi_batteri.append(nuovo)
        
        self.batteri.extend(nuovi_batteri)
        
        self.batteri = [b for b in self.batteri if b.vivo]

        nuovi_virus = []
        for virus in self.virus:
            if not virus.vivo:
                continue
            prob_morte_v = efficacia_antivirale * 0.01
            prob_morte_v *= fattore_opsonizzazione_virus
            if prob_morte_v > 0 and random.random() < prob_morte_v * dt_effettivo:
                virus.vivo = False
                continue
            virus.aggiorna(dt_effettivo, self.ambiente)
            if virus.pronto_duplicazione and len(self.virus) < 200:
                nv = virus.duplica()
                if nv:
                    nuovi_virus.append(nv)
        self.virus.extend(nuovi_virus)
        self.virus = [v for v in self.virus if v.vivo]
        
        patogeni_totali = len(self.batteri) + len(self.virus)
        if patogeni_totali > 20 and len(self.neutrofili) < 50:
            if random.random() < 0.01:  # 1% probabilità ogni frame
                x = random.randint(50, AREA_SIMULAZIONE_X - 50)
                y = random.randint(0, 100)  # Entrano dall'alto
                self.neutrofili.append(Neutrofilo(x, y))

        stats_for_log = self._raccogli_statistiche()
        stats_for_log["seed"] = self.seed
        self.logger.update(dt_effettivo, stats_for_log)
    
    def disegna(self):
        """Disegna tutto sullo schermo"""
        
        self.ambiente.disegna_sfondo(self.schermo)
        
        # Heatmap citochine (opzionale, commentato per performance)
        # self.ambiente.disegna_heatmap_citochine(self.schermo)
        
        for globulo in self.globuli_rossi:
            globulo.disegna(self.schermo)
        
        for batterio in self.batteri:
            batterio.disegna(self.schermo)
        
        for virus in self.virus:
            virus.disegna(self.schermo)
        
        for neutrofilo in self.neutrofili:
            neutrofilo.disegna(self.schermo)
        
        for macro in self.macrofagi:
            macro.disegna(self.schermo)
        
        for lt in self.linfo_t:
            lt.disegna(self.schermo)
        
        for lb in self.linfo_b:
            lb.disegna(self.schermo)
        
        pygame.draw.line(self.schermo, COLORE_UI_SEP_SIM_HUD, 
                        (AREA_SIMULAZIONE_X, 0), 
                        (AREA_SIMULAZIONE_X, ALTEZZA), 3)
        
        stats = self._raccogli_statistiche()
        self.hud.disegna(self.schermo, stats)
        
        if self.ui_screen != "sim":
            self._disegna_ui()
        
        if self.in_pausa:
            self._disegna_pausa()
        
        if self.tutorial_attivo and self.ui_screen == "sim":
            self._disegna_tutorial()
        
        pygame.display.flip()
    
    def _raccogli_statistiche(self):
        """Raccoglie statistiche per l'HUD"""
        return {
            'globuli_rossi': len(self.globuli_rossi),
            'neutrofili': len(self.neutrofili),
            'macrofagi': len(self.macrofagi),
            'linfo_t': len(self.linfo_t),
            'linfo_b': len(self.linfo_b),
            'batteri': len(self.batteri),
            'virus': len(self.virus),
            'patogeni_totali': len(self.batteri) + len(self.virus),
            'batteri_fagocitati': self.batteri_fagocitati_totali,
            'temperatura': self.ambiente.temperatura,
            'ossigeno': self.ambiente.ossigeno,
            'concentrazione_penicillina': self.gestore_farmaci.ottieni_concentrazione_totale('penicillina'),
            'efficacia_antibiotico': self.gestore_farmaci.ottieni_efficacia_antibiotico(),
            'concentrazione_oseltamivir': self.gestore_farmaci.ottieni_concentrazione_totale('oseltamivir'),
            'concentrazione_aciclovir': self.gestore_farmaci.ottieni_concentrazione_totale('aciclovir'),
            'efficacia_antivirale': self.gestore_farmaci.ottieni_efficacia_antivirale(),
            'anticorpi': self.ambiente.anticorpi,
            'velocita_simulazione': self.velocita_simulazione,
            'tempo_simulato': self.tempo_simulato
        }
    
    def _disegna_menu(self):
        """Disegna menu principale + tutorial/scenari"""
        overlay = pygame.Surface((AREA_SIMULAZIONE_X, AREA_SIMULAZIONE_Y), pygame.SRCALPHA)
        overlay.fill(COLORE_UI_MENU_SCRIM)
        self.schermo.blit(overlay, (0, 0))

        font_grande = brand_title_font(72)
        font_medio = subtitle_font(FONT_UI_SOTTOTITOLO)
        font_scenario = label_font(26)
        font_caption = caption_font(FONT_UI_MENU_FOOTER)

        titolo = font_grande.render("ImmunoMind", True, COLORE_BRAND_IMMUNOMIND)
        rect_titolo = titolo.get_rect(center=(AREA_SIMULAZIONE_X // 2, 140))
        self.schermo.blit(titolo, rect_titolo)

        sottotitolo = font_medio.render("Scenari & Tutorial (Innata + Adattativa)", True, COLORE_TIPO_SOTTOTITOLO)
        rect_sotto = sottotitolo.get_rect(center=(AREA_SIMULAZIONE_X // 2, 210))
        self._ui_blit_text_shadow(
            sottotitolo, rect_sotto.x, rect_sotto.y,
            shadow_alpha=UI_SOTTOTITOLO_OMBRA_ALPHA, offset=(2, 2),
        )

        y_inizio = 300
        scenarios = [
            ("batterica", "1) Batterica (E. coli)"),
            ("virale", "2) Virale (Influenza)"),
            ("vaccino", "3) Vaccino / Memoria"),
            ("ferita", "4) Ferita (infiammazione)"),
        ]

        lbl_grav = font_medio.render("Gravità:", True, COLORE_TIPO_ETICHETTA)
        val_grav = font_scenario.render(f"{self.gravita} / 5", True, COLORE_UI_ACCENT_CALDO)
        gx = AREA_SIMULAZIONE_X // 2 - (lbl_grav.get_width() + val_grav.get_width()) // 2
        self.schermo.blit(lbl_grav, (gx, y_inizio + 140))
        self.schermo.blit(val_grav, (gx + lbl_grav.get_width() + 8, y_inizio + 138))

        for idx, (key, label) in enumerate(scenarios):
            y = y_inizio + idx * 48
            is_sel = self.scenario_attivo == key
            color = COLORE_NEUTROFILO if is_sel else COLORE_TIPO_CORPO
            font_item = font_scenario if is_sel else body_font(26)
            arrow = "▶ " if is_sel else "  "
            testo = font_item.render(arrow + label, True, color)
            rect = testo.get_rect(center=(AREA_SIMULAZIONE_X // 2, y))
            self.schermo.blit(testo, rect)

    def _disegna_ui(self):
        """Disegna UI moderna a pagine (Home + Funzioni)."""
        overlay = pygame.Surface((LARGHEZZA, ALTEZZA), pygame.SRCALPHA)
        overlay.fill(COLORE_UI_OVERLAY)
        self.schermo.blit(overlay, (0, 0))

        grad = pygame.Surface((LARGHEZZA, ALTEZZA), pygame.SRCALPHA)
        for y in range(ALTEZZA):
            t = y / max(1, (ALTEZZA - 1))
            r = int(COLORE_UI_GRAD_LINE_TOP[0] + (COLORE_UI_GRAD_LINE_BOTTOM[0] - COLORE_UI_GRAD_LINE_TOP[0]) * t)
            g = int(COLORE_UI_GRAD_LINE_TOP[1] + (COLORE_UI_GRAD_LINE_BOTTOM[1] - COLORE_UI_GRAD_LINE_TOP[1]) * t)
            b = int(COLORE_UI_GRAD_LINE_TOP[2] + (COLORE_UI_GRAD_LINE_BOTTOM[2] - COLORE_UI_GRAD_LINE_TOP[2]) * t)
            a = int(COLORE_UI_GRAD_ALPHA_TOP + (COLORE_UI_GRAD_ALPHA_BOTTOM - COLORE_UI_GRAD_ALPHA_TOP) * t)
            pygame.draw.line(grad, (r, g, b, a), (0, y), (LARGHEZZA, y))
        self.schermo.blit(grad, (0, 0))

        mouse_pos = pygame.mouse.get_pos()

        font_title = brand_title_font(96)
        font_sub = subtitle_font(FONT_UI_SOTTOTITOLO)
        font_menu = ui_font(FONT_UI_MENU_PULSANTE, bold=True)
        font_nav = ui_font(FONT_UI_NAV, bold=True)
        font_footer = caption_font(FONT_UI_MENU_FOOTER)
        font_wiki_head = section_font(FONT_UI_WIKI_TITOLO)
        font_wiki_label = label_font(FONT_UI_WIKI_CORPO)
        font_wiki_body = body_font(FONT_UI_WIKI_CORPO)
        font_grav_digit = ui_font(FONT_UI_GRAV_DIGIT, bold=True)
        font_grav_legenda = label_font(FONT_UI_GRAV_LEGENDA)
        typo_fonts = {
            "title": section_font(FONT_UI_WIKI_TITOLO + 2),
            "section": font_wiki_head,
            "body": font_wiki_body,
            "caption": font_footer,
        }

        top_h = 64
        top_bg = pygame.Surface((LARGHEZZA, top_h), pygame.SRCALPHA)
        top_bg.fill(COLORE_UI_TOPBAR)
        self.schermo.blit(top_bg, (0, 0))
        pygame.draw.line(self.schermo, COLORE_UI_TOPBAR_LINE, (0, top_h), (LARGHEZZA, top_h), 2)

        self._ui_buttons.clear()
        nav_y = 14
        nav_w = 120
        nav_h = 36
        gap = 10
        labels = [("nav_scenari", "scenari"), ("nav_gravita", "gravità"), ("nav_wiki", "Wiki"), ("nav_info", "informazioni")]
        total_w = len(labels) * nav_w + (len(labels) - 1) * gap
        start_x = LARGHEZZA - total_w - 20
        for i, (key, lab) in enumerate(labels):
            rect = pygame.Rect(start_x + i * (nav_w + gap), nav_y, nav_w, nav_h)
            self._ui_make_button(key, rect, lab, kind="nav")
            self._ui_draw_button(key, font_nav, mouse_pos)

        if self.ui_screen == "home":
            titolo = font_title.render("ImmunoMind", True, COLORE_BRAND_IMMUNOMIND)
            rect_titolo = titolo.get_rect(center=(LARGHEZZA // 2, 260))
            self._ui_blit_text_shadow(titolo, rect_titolo.x, rect_titolo.y, shadow_alpha=130, offset=(3, 3))

            sottotitolo = font_sub.render("Simulatore Computazionale Sistema Immunitario", True, COLORE_TIPO_SOTTOTITOLO)
            rect_sotto = sottotitolo.get_rect(center=(LARGHEZZA // 2, 330))
            self._ui_blit_text_shadow(
                sottotitolo, rect_sotto.x, rect_sotto.y,
                shadow_alpha=UI_SOTTOTITOLO_OMBRA_ALPHA, offset=(2, 2),
            )

            start_rect = pygame.Rect(0, 0, 260, 54)
            start_rect.center = (LARGHEZZA // 2, 420)
            self._ui_make_button("start", start_rect, "START", kind="primary")
            self._ui_draw_button("start", font_menu, mouse_pos)

            if self._sim_ha_avviato_almeno_una_volta:
                resume_rect = pygame.Rect(0, 0, 260, 44)
                resume_rect.center = (LARGHEZZA // 2, 485)
                self._ui_make_button("resume", resume_rect, "RIPRENDI", kind="secondary")
                self._ui_draw_button("resume", ui_font(22, bold=True), mouse_pos)

            hint = font_footer.render("Suggerimento: configura scenari/gravità dal menu in alto.", True, COLORE_TIPO_MUTED)
            hint_rect = hint.get_rect(center=(LARGHEZZA // 2, 545))
            self._ui_blit_text_shadow(hint, hint_rect.x, hint_rect.y, shadow_alpha=110, offset=(2, 2))

        elif self.ui_screen == "scenari":
            titolo_bottom = self._ui_draw_page_title("Scenari", 60, top_h + 22)
            base_y = titolo_bottom + 20

            bw, bh = 440, 50
            items = [
                ("sc_batterica", "Batterica (E. coli)", "batterica"),
                ("sc_virale", "Virale (Influenza)", "virale"),
                ("sc_vaccino", "Vaccino / Memoria", "vaccino"),
                ("sc_ferita", "Ferita (infiammazione)", "ferita"),
            ]
            for i, (key, label, value) in enumerate(items):
                r = pygame.Rect(0, 0, bw, bh)
                r.topleft = (60, base_y + i * (bh + 14))
                kind = "primary" if self.scenario_attivo == value else "secondary"
                self._ui_make_button(key, r, label, kind=kind)
                self._ui_draw_button(key, font_menu, mouse_pos)

            back_rect = pygame.Rect(60, ALTEZZA - 90, 160, 46)
            self._ui_make_button("back", back_rect, "Indietro", kind="nav")
            self._ui_draw_button("back", font_menu, mouse_pos)

            start_rect = pygame.Rect(LARGHEZZA - 60 - 240, ALTEZZA - 90, 240, 46)
            self._ui_make_button("start_from_scenari", start_rect, "Start", kind="primary")
            self._ui_draw_button("start_from_scenari", font_menu, mouse_pos)

            st = font_footer.render(f"Selezionato: {self.scenario_attivo} | Gravità: {self.gravita}/5", True, COLORE_TIPO_MUTED)
            self._ui_blit_text_shadow(st, 60, ALTEZZA - 130, shadow_alpha=110, offset=(2, 2))

        elif self.ui_screen == "gravita":
            titolo_bottom = self._ui_draw_page_title("Gravità", 60, top_h + 22)
            base_y = titolo_bottom + 26
            btn_sz = 48

            minus_rect = pygame.Rect(60, base_y, btn_sz, btn_sz)
            plus_rect = pygame.Rect(60 + btn_sz + 12, base_y, btn_sz, btn_sz)
            self._ui_make_button("grav_minus", minus_rect, "−", kind="primary")
            self._ui_make_button("grav_plus", plus_rect, "+", kind="primary")
            self._ui_draw_button("grav_minus", font_grav_digit, mouse_pos)
            self._ui_draw_button("grav_plus", font_grav_digit, mouse_pos)

            label = font_grav_legenda.render("Livello attuale:", True, COLORE_TIPO_ETICHETTA)
            val = font_grav_digit.render(f"{self.gravita} / 5", True, COLORE_TIPO_VALORE)
            self._ui_blit_text_shadow(label, 60, base_y + btn_sz + 12, shadow_alpha=120, offset=(2, 2))
            self._ui_blit_text_shadow(
                val, 60 + label.get_width() + 10, base_y + btn_sz + 10, shadow_alpha=120, offset=(2, 2)
            )

            bw, bh = 54, 48
            row_y = base_y + btn_sz + 12 + label.get_height() + 16
            for i in range(1, 6):
                r = pygame.Rect(60 + (i - 1) * (bw + 12), row_y, bw, bh)
                kind = "primary" if self.gravita == i else "secondary"
                self._ui_make_button(f"grav_{i}", r, str(i), kind=kind)
                self._ui_draw_button(f"grav_{i}", font_grav_digit, mouse_pos)

            back_rect = pygame.Rect(60, ALTEZZA - 90, 160, 46)
            self._ui_make_button("back", back_rect, "Indietro", kind="nav")
            self._ui_draw_button("back", font_menu, mouse_pos)

            start_rect = pygame.Rect(LARGHEZZA - 60 - 240, ALTEZZA - 90, 240, 46)
            self._ui_make_button("start_from_gravita", start_rect, "Start", kind="primary")
            self._ui_draw_button("start_from_gravita", font_menu, mouse_pos)

            st = font_footer.render(f"Scenario: {self.scenario_attivo}", True, COLORE_TIPO_MUTED)
            self._ui_blit_text_shadow(st, 60, ALTEZZA - 130, shadow_alpha=110, offset=(2, 2))

        elif self.ui_screen == "wiki":
            titolo_bottom = self._ui_draw_page_title("Wiki", 60, top_h + 22)
            content_top = titolo_bottom + 12
            wiki = [(s["title"], s["paragraphs"]) for s in WIKI_SECTIONS]

            content_bottom = ALTEZZA - 110
            viewport = pygame.Rect(60, content_top, LARGHEZZA - 120, content_bottom - content_top)
            pygame.draw.rect(self.schermo, COLORE_UI_WIKI_BORDO, viewport, width=1, border_radius=12)

            self._wiki_hitboxes = []
            y = viewport.y + 16 - self._wiki_scroll
            max_w = viewport.width - 32
            line_h = 22
            title_h = 28

            for idx, (title, paragraphs) in enumerate(wiki):
                header_rect = pygame.Rect(viewport.x + 12, y, viewport.width - 24, title_h)
                if header_rect.bottom >= viewport.y - 30 and header_rect.top <= viewport.bottom + 30:
                    is_open = idx in self._wiki_open
                    toggle = "▾" if is_open else "▸"
                    title_color = COLORE_TIPO_SEZIONE
                    t_title = font_wiki_head.render(f"{toggle}  {title}", True, title_color)
                    self._ui_blit_text_shadow(t_title, header_rect.x, header_rect.y, shadow_alpha=140, offset=(2, 2))
                    self._wiki_hitboxes.append((header_rect, idx))
                y += title_h + 6

                if idx in self._wiki_open:
                    for p in paragraphs:
                        words = p.split(" ")
                        line = ""
                        for w in words:
                            test = (line + " " + w).strip()
                            if font_wiki_body.size(test)[0] <= max_w:
                                line = test
                            else:
                                if viewport.y - 30 <= y <= viewport.bottom + 30:
                                    self._wiki_blit_line_colored(
                                        line, viewport.x + 18, y, font_wiki_body, font_wiki_label
                                    )
                                y += line_h
                                line = w
                        if line:
                            if viewport.y - 30 <= y <= viewport.bottom + 30:
                                self._wiki_blit_line_colored(
                                    line, viewport.x + 18, y, font_wiki_body, font_wiki_label
                                )
                            y += line_h
                        y += 10
                y += 6

            content_height = (y - (viewport.y + 16)) + self._wiki_scroll
            self._wiki_scroll_max = max(0, int(content_height - viewport.height + 20))

            back_rect = pygame.Rect(60, ALTEZZA - 90, 160, 46)
            self._ui_make_button("back", back_rect, "Indietro", kind="nav")
            self._ui_draw_button("back", font_menu, mouse_pos)

        elif self.ui_screen == "info":
            titolo_bottom = self._ui_draw_page_title("Informazioni", 60, top_h + 22, FONT_UI_PAGE_TITLE_LUNGO)
            y = titolo_bottom + 16

            lines = [
                ("title", "ImmunoMind — simulatore del sistema immunitario"),
                ("body", "Modello semplificato a scopo didattico."),
                ("blank", ""),
                ("section", "Tasti (in simulazione)"),
                ("body", "Click — aggiunge patogeni (batteri o virus in base allo scenario)"),
                ("body", "SPAZIO — pausa"),
                ("body", "ESC — torna alla Home"),
                ("body", "1 — Penicillina (antibiotico)"),
                ("body", "2 — Oseltamivir (antivirale)"),
                ("body", "3 — Aciclovir (antivirale didattico)"),
                ("body", "+ / − — velocità simulazione"),
                ("body", "R — reset"),
                ("body", "E — esporta dati CSV (se disponibili)"),
                ("blank", ""),
                ("section", "Sviluppo"),
                ("body", crediti_brevi()),
                ("caption", COPYRIGHT),
                ("blank", ""),
                ("section", "Impostazioni correnti"),
                ("caption", f"Scenario: {self.scenario_attivo}  ·  Gravità: {self.gravita}/5  ·  Seed: {self.seed}"),
                ("caption", f"Versione {VERSIONE}"),
            ]

            for kind, line in lines:
                y = self._ui_draw_typo_line(kind, line, 60, y, typo_fonts)

            back_rect = pygame.Rect(60, ALTEZZA - 90, 160, 46)
            self._ui_make_button("back", back_rect, "Indietro", kind="nav")
            self._ui_draw_button("back", font_menu, mouse_pos)

    def _avvia_tutorial(self):
        """Avvia una guida contestuale basata sullo scenario scelto."""
        self.tutorial_attivo = True
        self.tutorial_step = 0
        self.tutorial_start_ms = pygame.time.get_ticks()
        step_ms = 4500
        self.tutorial_step_ms = step_ms
        
        if self.scenario_attivo == "batterica":
            self.tutorial_testi = [
                "Scenario Batterica (Innate + Antibiotico)",
                "Click: aggiunge batteri (gialli). Guarda neutrofili (blu) inseguire e fagocitare.",
                "Quando i batteri aumentano, usa Penicillina: tasto 1.",
                "Obiettivo: ridurre i batteri a 0 e osservare la caduta della febbre.",
            ]
        elif self.scenario_attivo == "virale":
            self.tutorial_testi = [
                "Scenario Virale (Influenza - modello semplificato)",
                "Click: aggiunge virus (arancioni). Neutrofili sono meno efficaci sui virus.",
                "Antibiotico (1) non risolve il problema nei virus: usa Oseltamivir (2).",
                "Quando entrano i linfociti T (viola), vedrai una clearance più efficace.",
            ]
        elif self.scenario_attivo == "vaccino":
            self.tutorial_testi = [
                "Scenario Vaccino / Memoria",
                "Hai anticorpi iniziali: la risposta adattativa parte più in fretta.",
                "Click: aggiunge batteri. Confronta con scenario batterica standard.",
                "Obiettivo: risposta più rapida (B → anticorpi).",
            ]
        else:
            self.tutorial_testi = [
                "Scenario Ferita / Infiammazione",
                "Citochine alte: più segnali di allarme nell'ambiente.",
                "Neutrofili e macrofagi aumentano l'attacco sui patogeni.",
                "Se l'infezione peggiora, usa Penicillina: tasto 1.",
            ]

    def _disegna_tutorial(self):
        """Mostra overlay tutorial per i primi step del run."""
        if not self.tutorial_attivo:
            return
        
        elapsed = pygame.time.get_ticks() - self.tutorial_start_ms
        if elapsed < 0:
            return
        
        step = int(elapsed / self.tutorial_step_ms)
        if step >= len(self.tutorial_testi):
            self.tutorial_attivo = False
            return
        
        testo = self.tutorial_testi[step]
        rect = pygame.Rect(40, 90, AREA_SIMULAZIONE_X - 80, 120)
        pygame.draw.rect(self.schermo, COLORE_UI_TUTORIAL_BG, rect, border_radius=10)
        pygame.draw.rect(self.schermo, COLORE_UI_TUTORIAL_BORDO, rect, width=2, border_radius=10)
        
        font_big = section_font(28)
        font_small = body_font(22)
        t_big = font_big.render(f"TUTORIAL ({step+1}/{len(self.tutorial_testi)})", True, COLORE_TIPO_SEZIONE)
        t_txt = font_small.render(testo, True, COLORE_TIPO_CORPO)
        
        self.schermo.blit(t_big, (rect.x + 10, rect.y + 8))
        self.schermo.blit(t_txt, (rect.x + 10, rect.y + 40))
    
    def _disegna_pausa(self):
        """Disegna indicatore di pausa"""
        font = section_font(48)
        testo = font.render("PAUSA", True, COLORE_TIPO_SEZIONE)
        rect = testo.get_rect(center=(AREA_SIMULAZIONE_X // 2, 50))
        
        sfondo = pygame.Surface((rect.width + 40, rect.height + 20), pygame.SRCALPHA)
        sfondo.fill(COLORE_UI_PAUSA_BG)
        self.schermo.blit(sfondo, (rect.x - 20, rect.y - 10))
        
        self.schermo.blit(testo, rect)
    
    def esegui(self):
        """Avvia il loop principale finché l'utente non chiude la finestra."""
        print("=" * 60)
        print(riga_avvio_console())
        print(COPYRIGHT)
        print("=" * 60)
        print("\nSimulazione avviata.")
        print("ESC → Home  ·  Click → patogeni  ·  1/2/3 → farmaci\n")

        while self.in_esecuzione:
            dt = self.clock.tick(FPS) / 1000.0
            self.gestisci_input()
            self.aggiorna(dt)
            self.disegna()

        pygame.quit()
        if self.logger and self.logger.has_data():
            path = self.logger.export_csv(note="auto")
            print(f"\nDati salvati in: {path}")
        print(f"\nGrazie per aver usato {PROGETTO}! — {MARCHIO}\n")


def main():
    """Punto di ingresso quando lanci python main.py"""
    try:
        simulatore = ImmunoMind()
        simulatore.esegui()
    except Exception as e:
        print(f"\nErrore durante l'esecuzione: {e}")
        print(f"Segnala il problema a {AUTORE} ({MARCHIO}) includendo il messaggio sopra.\n")
        import traceback
        traceback.print_exc()
        pygame.quit()
        sys.exit(1)


if __name__ == "__main__":
    main()

