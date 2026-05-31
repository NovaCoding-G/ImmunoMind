"""Font di sistema con cache. © G.Roscino / NovaCoding."""

import pygame

_cache = {}


def ui_font(size: int, bold: bool = False) -> pygame.font.Font:
    pygame.font.init()
    key = (size, bold)
    if key in _cache:
        return _cache[key]

    famiglie = (
        ["Segoe UI Semibold", "Segoe UI", "Calibri", "Arial"]
        if bold
        else ["Segoe UI", "Calibri", "Arial"]
    )
    for famiglia in famiglie:
        try:
            font = pygame.font.SysFont(famiglia, size, bold=bold)
            if font.get_height() > 0:
                _cache[key] = font
                return font
        except Exception:
            continue

    font = pygame.font.Font(None, size)
    _cache[key] = font
    return font


def brand_title_font(size: int) -> pygame.font.Font:
    return ui_font(size, bold=True)


def subtitle_font(size: int) -> pygame.font.Font:
    return ui_font(size, bold=True)


def section_font(size: int) -> pygame.font.Font:
    return ui_font(size, bold=True)


def label_font(size: int) -> pygame.font.Font:
    return ui_font(size, bold=True)


def body_font(size: int) -> pygame.font.Font:
    return ui_font(size, bold=False)


def caption_font(size: int) -> pygame.font.Font:
    return ui_font(size, bold=False)
