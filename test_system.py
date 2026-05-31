"""
ImmunoMind — verifica che tutto sia installato correttamente.

Lancia questo script prima del primo avvio: controlla librerie,
moduli del progetto e un mini-run della simulazione.

Sviluppato da G.Roscino · NovaCoding
© 2026 G.Roscino / NovaCoding. Tutti i diritti riservati.
"""

import sys

from brand import MARCHIO, AUTORE, PROGETTO, COPYRIGHT, riga_avvio_console

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

def test_importazioni():
    """Testa se tutte le librerie necessarie sono installate"""
    print("🔍 Test 1: Verifica importazioni...")
    
    errori = []
    
    try:
        import pygame
        print(f"  ✅ pygame {pygame.version.ver} installato")
    except ImportError:
        print("  ❌ pygame NON trovato")
        errori.append("pygame")
    
    try:
        import numpy as np
        print(f"  ✅ numpy {np.__version__} installato")
    except ImportError:
        print("  ❌ numpy NON trovato")
        errori.append("numpy")
    
    try:
        import matplotlib
        print(f"  ✅ matplotlib {matplotlib.__version__} installato")
    except ImportError:
        print("  ❌ matplotlib NON trovato")
        errori.append("matplotlib")
    
    return errori


def test_moduli_progetto():
    """Testa se tutti i file del progetto sono presenti"""
    print("\n🔍 Test 2: Verifica moduli progetto...")
    
    errori = []
    
    try:
        import config
        print(f"  ✅ config.py caricato")
        print(f"     - Larghezza: {config.LARGHEZZA}px")
        print(f"     - Altezza: {config.ALTEZZA}px")
        print(f"     - FPS: {config.FPS}")
    except ImportError as e:
        print(f"  ❌ config.py: {e}")
        errori.append("config.py")
    
    try:
        from entities import GlobuloRosso, Neutrofilo, Batterio
        print(f"  ✅ entities.py caricato")
        print(f"     - GlobuloRosso: OK")
        print(f"     - Neutrofilo: OK")
        print(f"     - Batterio: OK")
    except ImportError as e:
        print(f"  ❌ entities.py: {e}")
        errori.append("entities.py")
    
    try:
        from environment import Ambiente, GestoreFarmaci
        print(f"  ✅ environment.py caricato")
    except ImportError as e:
        print(f"  ❌ environment.py: {e}")
        errori.append("environment.py")
    
    try:
        from hud import HUD
        print(f"  ✅ hud.py caricato")
    except ImportError as e:
        print(f"  ❌ hud.py: {e}")
        errori.append("hud.py")
    
    return errori


def test_creazione_entita():
    """Testa la creazione di entità base"""
    print("\n🔍 Test 3: Creazione entità...")
    
    try:
        from entities import GlobuloRosso, Neutrofilo, Batterio
        from environment import Ambiente
        
        globulo = GlobuloRosso(100, 100)
        neutrofilo = Neutrofilo(200, 200)
        batterio = Batterio(300, 300)
        ambiente = Ambiente()
        
        print(f"  ✅ GlobuloRosso creato: pos=({globulo.x}, {globulo.y}), dim={globulo.dimensione}")
        print(f"  ✅ Neutrofilo creato: pos=({neutrofilo.x}, {neutrofilo.y}), stato={neutrofilo.stato}")
        print(f"  ✅ Batterio creato: pos=({batterio.x}, {batterio.y}), energia={batterio.energia}")
        print(f"  ✅ Ambiente creato: temp={ambiente.temperatura}°C")
        
        return []
    except Exception as e:
        print(f"  ❌ Errore creazione entità: {e}")
        return ["creazione_entita"]


def test_simulazione_base():
    """Testa una breve simulazione"""
    print("\n🔍 Test 4: Simulazione base...")
    
    try:
        from entities import Neutrofilo, Batterio
        from environment import Ambiente
        
        ambiente = Ambiente()
        neutrofilo = Neutrofilo(100, 100)
        batterio = Batterio(110, 110)
        
        for i in range(10):
            neutrofilo.rileva_patogeni([batterio])
            neutrofilo.aggiorna(0.016, ambiente)
            batterio.aggiorna(0.016, ambiente)
        
        print(f"  ✅ Simulazione 10 frame completata")
        print(f"     - Neutrofilo: stato={neutrofilo.stato}, vivo={neutrofilo.vivo}")
        print(f"     - Batterio: vivo={batterio.vivo}, energia={batterio.energia:.1f}")
        
        if neutrofilo.stato == "inseguimento":
            print(f"  ✅ Chemotassi funziona! Neutrofilo sta inseguendo")
        else:
            print(f"  ⚠️  Neutrofilo non ha rilevato batterio (potrebbe essere normale)")
        
        return []
    except Exception as e:
        print(f"  ❌ Errore simulazione: {e}")
        import traceback
        traceback.print_exc()
        return ["simulazione"]


def test_pygame_init():
    """Testa inizializzazione pygame"""
    print("\n🔍 Test 5: Inizializzazione pygame...")
    
    try:
        import pygame
        pygame.init()
        
        pygame.font.init()
        font = pygame.font.Font(None, 24)
        print(f"  ✅ Pygame inizializzato")
        print(f"  ✅ Font disponibili: {pygame.font.get_fonts()[:3]}...")
        
        info = pygame.display.Info()
        print(f"  ✅ Display: {info.current_w}x{info.current_h}")
        
        pygame.quit()
        return []
    except Exception as e:
        print(f"  ❌ Errore pygame: {e}")
        return ["pygame_init"]


def stampa_riepilogo(tutti_errori):
    """Stampa riepilogo finale"""
    print("\n" + "="*70)
    
    if not tutti_errori:
        print("✅ TUTTI I TEST SUPERATI!")
        print("\n🎉 ImmunoMind è pronto per essere avviato!")
        print("\n📝 Per avviare il simulatore:")
        print("   python main.py")
        print("\n📚 Leggi README.md per istruzioni complete")
        print("🧪 Esperimenti guidati: docs/EXPERIMENTS.md (IT + EN)")
    else:
        print("❌ ALCUNI TEST HANNO FALLITO")
        print(f"\n⚠️  Problemi rilevati: {', '.join(set(tutti_errori))}")
        print("\n🔧 Soluzioni:")
        
        if any(lib in tutti_errori for lib in ['pygame', 'numpy', 'matplotlib']):
            print("\n  Per installare le librerie mancanti:")
            print("    pip install -r requirements.txt")
            print("  oppure:")
            print("    pip install pygame numpy matplotlib")
        
        if any('.py' in err for err in tutti_errori):
            print("\n  File di progetto mancanti o corrotti.")
            print("  Verifica che tutti i file siano presenti nella cartella.")
        
        print("\n  Per problemi persistenti contatta:")
        print(f"  {AUTORE} — {MARCHIO}")
    
    print("="*70)


def main():
    """Esegue tutti i controlli e stampa un riepilogo."""
    print("\n" + "=" * 70)
    print(f"Verifica sistema — {PROGETTO}")
    print(riga_avvio_console())
    print(COPYRIGHT)
    print("=" * 70)
    print(f"Python: {sys.version}")
    print("=" * 70 + "\n")
    
    tutti_errori = []
    
    tutti_errori.extend(test_importazioni())
    tutti_errori.extend(test_moduli_progetto())
    tutti_errori.extend(test_creazione_entita())
    tutti_errori.extend(test_simulazione_base())
    tutti_errori.extend(test_pygame_init())
    
    stampa_riepilogo(tutti_errori)
    
    return 0 if not tutti_errori else 1


if __name__ == "__main__":
    sys.exit(main())

