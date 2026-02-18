"""
Shared UI drawing utilities.
"""
import pygame
from src.constants import *
from src.localization import t


def get_font(size: int, bold: bool = False) -> pygame.font.Font:
    try:
        return pygame.font.SysFont("segoeui", size, bold=bold)
    except Exception:
        return pygame.font.Font(None, size)


def draw_text(surface, text: str, x: int, y: int, font: pygame.font.Font,
              color=WHITE, center=False, shadow=True):
    if shadow:
        shadow_surf = font.render(text, True, (0, 0, 0))
        sr = shadow_surf.get_rect()
        if center:
            sr.center = (x + 1, y + 1)
        else:
            sr.topleft = (x + 1, y + 1)
        surface.blit(shadow_surf, sr)
    surf = font.render(text, True, color)
    r = surf.get_rect()
    if center:
        r.center = (x, y)
    else:
        r.topleft = (x, y)
    surface.blit(surf, r)
    return r


def draw_bar(surface, x, y, w, h, current, maximum, fg_color, bg_color=None, label=""):
    bg_color = bg_color or (40, 40, 40)
    pygame.draw.rect(surface, bg_color, (x, y, w, h), border_radius=4)
    if maximum > 0:
        fill_w = int(w * max(0, current) / maximum)
        if fill_w > 0:
            pygame.draw.rect(surface, fg_color, (x, y, fill_w, h), border_radius=4)
    pygame.draw.rect(surface, (80, 80, 80), (x, y, w, h), 1, border_radius=4)
    if label:
        font = get_font(14)
        draw_text(surface, label, x + w // 2, y + h // 2, font, WHITE, center=True, shadow=False)


def draw_panel(surface, x, y, w, h, color=PANEL_BG, border_color=CARD_BORDER, radius=10):
    pygame.draw.rect(surface, color, (x, y, w, h), border_radius=radius)
    pygame.draw.rect(surface, border_color, (x, y, w, h), 2, border_radius=radius)


def draw_button(surface, rect: pygame.Rect, text: str, font: pygame.font.Font,
                color=PANEL_BG, hover_color=CARD_HOVER, border_color=CARD_BORDER,
                text_color=WHITE, mouse_pos=None, radius=8) -> bool:
    """Draw a button. Returns True if mouse is hovering."""
    hovering = rect.collidepoint(mouse_pos) if mouse_pos else False
    bg = hover_color if hovering else color
    pygame.draw.rect(surface, bg, rect, border_radius=radius)
    pygame.draw.rect(surface, border_color, rect, 2, border_radius=radius)
    draw_text(surface, text, rect.centerx, rect.centery, font, text_color, center=True)
    return hovering


def draw_status_icons(surface, statuses, x, y, font_small):
    """Draw status effect icons in a row."""
    for i, s in enumerate(statuses):
        col = s.color if hasattr(s, 'color') else GREY
        rx = x + i * 38
        pygame.draw.rect(surface, col, (rx, y, 34, 20), border_radius=4)
        translated_name = t("status." + s.name)
        draw_text(surface, f"{translated_name[:3]}{s.stacks}", rx + 2, y + 2,
                  font_small, WHITE, shadow=False)


def wrap_text(text: str, font: pygame.font.Font, max_width: int) -> list[str]:
    words = text.split()
    lines = []
    current = ""
    for word in words:
        test = (current + " " + word).strip()
        if font.size(test)[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines
