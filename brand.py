"""Marchio e metadati del progetto."""

MARCHIO = "NovaCoding"
AUTORE = "G.Roscino"
PROGETTO = "ImmunoMind"
VERSIONE = "1.0.0"
ANNO_COPYRIGHT = 2026

COPYRIGHT = f"© {ANNO_COPYRIGHT} {AUTORE} / {MARCHIO}. Tutti i diritti riservati."


def riga_avvio_console() -> str:
    return f"{PROGETTO} v{VERSIONE}  ·  {MARCHIO}  ·  {AUTORE}"


def crediti_brevi() -> str:
    return f"Sviluppato da {AUTORE} — {MARCHIO}"
