"""HUD laterale. © G.Roscino / NovaCoding."""

import pygame
from config import *
from fonts import brand_title_font, section_font, label_font, body_font, caption_font
from brand import MARCHIO, AUTORE


class HUD:

    def __init__(self):
        pygame.font.init()
        self.font_brand = brand_title_font(FONT_HUD_BRAND)
        self.font_sezione = section_font(FONT_HUD_SEZIONE)
        self.font_etichetta = label_font(FONT_HUD_ETICHETTA)
        self.font_valore = label_font(FONT_HUD_VALORE)
        self.font_corpo = body_font(FONT_SIZE_TESTO)
        self.font_caption = caption_font(FONT_SIZE_PICCOLO)

        self.x = AREA_SIMULAZIONE_X + HUD_PADDING
        self.y = HUD_PADDING
        self.larghezza = HUD_LARGHEZZA - HUD_PADDING * 2

    def _wrap_lines(self, font, text, max_width):
        words = text.split(" ")
        lines = []
        line = ""
        for w in words:
            test = (line + " " + w).strip()
            if font.size(test)[0] <= max_width:
                line = test
            else:
                if line:
                    lines.append(line)
                line = w
        if line:
            lines.append(line)
        return lines

    def _disegna_riga_chiave_valore(self, schermo, y, chiave, valore, colore_valore=None):
        if colore_valore is None:
            colore_valore = COLORE_TIPO_VALORE
        lbl = self.font_etichetta.render(f"{chiave}:", True, COLORE_TIPO_ETICHETTA)
        val = self.font_valore.render(str(valore), True, colore_valore)
        schermo.blit(lbl, (self.x, y))
        schermo.blit(val, (self.x + lbl.get_width() + 8, y))
        return y + 25

    def disegna(self, schermo, stats):
        sfondo = pygame.Surface((HUD_LARGHEZZA, ALTEZZA), pygame.SRCALPHA)
        sfondo.fill(COLORE_HUD_BG)
        schermo.blit(sfondo, (AREA_SIMULAZIONE_X, 0))

        y_corrente = self.y

        titolo = self.font_brand.render("ImmunoMind", True, COLORE_BRAND_IMMUNOMIND)
        titolo_x = self.x + 6
        titolo_y = max(4, self.y - 12)
        schermo.blit(titolo, (titolo_x, titolo_y))
        y_corrente = titolo_y + titolo.get_height() + 10

        pygame.draw.line(
            schermo,
            COLORE_UI_HUD_SEP,
            (self.x, y_corrente),
            (self.x + self.larghezza, y_corrente),
            2,
        )
        y_corrente += 20

        y_corrente = self._disegna_sezione(schermo, "POPOLAZIONE", y_corrente)
        y_corrente = self._disegna_contatore(
            schermo, "Globuli Rossi", stats["globuli_rossi"], COLORE_GLOBULO_ROSSO, y_corrente
        )
        y_corrente = self._disegna_contatore(
            schermo, "Neutrofili", stats["neutrofili"], COLORE_NEUTROFILO, y_corrente
        )
        y_corrente = self._disegna_contatore(
            schermo, "Macrofagi", stats.get("macrofagi", 0), COLORE_MACROFAGO, y_corrente
        )
        y_corrente = self._disegna_contatore(
            schermo, "Linfociti T", stats.get("linfo_t", 0), COLORE_LINFOCITA_T, y_corrente
        )
        y_corrente = self._disegna_contatore(
            schermo, "Linfociti B", stats.get("linfo_b", 0), COLORE_LINFOCITA_B, y_corrente
        )
        y_corrente = self._disegna_contatore(
            schermo, "Virus", stats.get("virus", 0), COLORE_VIRUS, y_corrente
        )
        y_corrente += 10

        y_corrente = self._disegna_sezione(schermo, "PATOGENI", y_corrente)
        y_corrente = self._disegna_contatore(
            schermo, "Batteri", stats["batteri"], COLORE_BATTERIO, y_corrente
        )
        cfu = stats["batteri"] * 1000000
        testo_cfu = self.font_caption.render(f"Carica: {cfu:,} CFU/ml", True, COLORE_TIPO_MUTED)
        schermo.blit(testo_cfu, (self.x + 20, y_corrente))
        y_corrente += 25

        y_corrente = self._disegna_sezione(schermo, "AMBIENTE", y_corrente)
        temp = stats["temperatura"]
        colore_temp = COLORE_TIPO_VALORE if temp < 38 else COLORE_UI_HUD_TEMP_FEBBRE
        y_corrente = self._disegna_riga_chiave_valore(
            schermo, y_corrente, "Temperatura", f"{temp:.1f}°C", colore_temp
        )
        barra_width = int((temp - 36) / (42 - 36) * self.larghezza)
        pygame.draw.rect(
            schermo, COLORE_UI_HUD_BARRA_SFONDO, (self.x, y_corrente, self.larghezza, 10)
        )
        pygame.draw.rect(
            schermo, colore_temp, (self.x, y_corrente, max(0, barra_width), 10)
        )
        y_corrente += 20
        y_corrente = self._disegna_riga_chiave_valore(
            schermo, y_corrente, "Ossigeno", f"{stats['ossigeno']:.0f}%", COLORE_TIPO_VALORE
        )
        y_corrente += 5

        y_corrente = self._disegna_sezione(schermo, "FARMACI / ANTICORPI", y_corrente)
        penicillina = stats["concentrazione_penicillina"]
        efficacia = stats["efficacia_antibiotico"] * 100
        y_corrente = self._disegna_riga_chiave_valore(
            schermo, y_corrente, "Penicillina", f"{penicillina:.1f} mg/L", COLORE_TIPO_VALORE
        )
        testo_eff = self.font_caption.render(
            f"Efficacia: {efficacia:.0f}%", True, COLORE_UI_HUD_EFFICACIA_OK
        )
        schermo.blit(testo_eff, (self.x + 20, y_corrente))
        y_corrente += 22

        oselt = stats.get("concentrazione_oseltamivir", 0.0)
        acic = stats.get("concentrazione_aciclovir", 0.0)
        antivirale = stats.get("efficacia_antivirale", 0.0) * 100
        y_corrente = self._disegna_riga_chiave_valore(
            schermo, y_corrente, "Oseltamivir", f"{oselt:.1f} mg/L", COLORE_TIPO_VALORE
        )
        y_corrente = self._disegna_riga_chiave_valore(
            schermo, y_corrente, "Aciclovir", f"{acic:.1f} mg/L", COLORE_TIPO_VALORE
        )
        testo_antiv = self.font_caption.render(
            f"Efficacia antivirale: {antivirale:.0f}%", True, COLORE_UI_HUD_ANTIVIR
        )
        schermo.blit(testo_antiv, (self.x + 20, y_corrente))
        y_corrente += 22

        anticorpi = stats.get("anticorpi", 0.0)
        perc_ab = min(100, int(anticorpi / LIMITE_ANTICORPI * 100))
        y_corrente = self._disegna_riga_chiave_valore(
            schermo, y_corrente, "Anticorpi", f"{perc_ab:.0f}%", COLORE_ANTICORPO
        )
        barra_ab = int(self.larghezza * perc_ab / 100)
        pygame.draw.rect(
            schermo, COLORE_UI_HUD_BARRA_AB_SFONDO, (self.x, y_corrente, self.larghezza, 8)
        )
        pygame.draw.rect(
            schermo, COLORE_ANTICORPO, (self.x, y_corrente, max(0, barra_ab), 8)
        )
        y_corrente += 20

        y_corrente = self._disegna_sezione(schermo, "RISPOSTA IMMUNITARIA", y_corrente)
        patogeni_totali = stats.get("patogeni_totali", stats.get("batteri", 0))
        if patogeni_totali == 0:
            fase = "SALUTE"
            colore_fase = COLORE_UI_HUD_FASE_SALUTE
        elif patogeni_totali < 20:
            fase = "INNATA ATTIVA"
            colore_fase = COLORE_UI_HUD_FASE_INNATA
        else:
            fase = "INFEZIONE GRAVE"
            colore_fase = COLORE_UI_HUD_FASE_GRAVE
        y_corrente = self._disegna_riga_chiave_valore(
            schermo, y_corrente, "Stato", fase, colore_fase
        )
        testo_fago = self.font_caption.render(
            f"Fagocitosi: {stats['batteri_fagocitati']}", True, COLORE_TIPO_CORPO
        )
        schermo.blit(testo_fago, (self.x + 20, y_corrente))
        y_corrente += 22

        y_corrente += 6
        vel = stats["velocita_simulazione"]
        testo_vel = self.font_caption.render(
            f"Velocità: {vel}x", True, COLORE_UI_HUD_VELOCITA
        )
        schermo.blit(testo_vel, (self.x, y_corrente))
        y_corrente += 22
        tempo_min = int(stats["tempo_simulato"] / 60)
        tempo_sec = int(stats["tempo_simulato"] % 60)
        testo_tempo = self.font_caption.render(
            f"Tempo: {tempo_min:02d}:{tempo_sec:02d}", True, COLORE_TIPO_MUTED
        )
        schermo.blit(testo_tempo, (self.x, y_corrente))
        y_corrente += 22

        firma = self.font_caption.render(f"{MARCHIO} · {AUTORE}", True, COLORE_TIPO_MUTED)
        schermo.blit(firma, (self.x, ALTEZZA - HUD_PADDING - firma.get_height() - 4))

    def _disegna_sezione(self, schermo, titolo, y):
        testo = self.font_sezione.render(titolo, True, COLORE_TIPO_SEZIONE)
        schermo.blit(testo, (self.x, y))
        pygame.draw.line(
            schermo,
            COLORE_UI_HUD_SEP,
            (self.x, y + testo.get_height() + 4),
            (self.x + self.larghezza, y + testo.get_height() + 4),
            1,
        )
        return y + 30

    def _disegna_contatore(self, schermo, etichetta, valore, colore, y):
        testo_label = self.font_etichetta.render(etichetta, True, COLORE_TIPO_ETICHETTA)
        schermo.blit(testo_label, (self.x, y))
        testo_valore = self.font_valore.render(str(valore), True, colore)
        schermo.blit(testo_valore, (self.x + 200, y))
        pygame.draw.circle(schermo, colore, (self.x + self.larghezza - 10, y + 8), 6)
        return y + 25

    def handle_click(self, pos):
        return
