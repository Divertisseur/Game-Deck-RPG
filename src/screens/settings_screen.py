"""
Settings Screen - Language selection.
"""
import pygame
from src.constants import *
from src.screens.ui_utils import draw_text, draw_button, draw_panel, get_font
from src.localization import t, set_language, LANG_EN, LANG_FR

class SettingsScreen:
    def __init__(self):
        self.font_title = get_font(48, bold=True)
        self.font_label = get_font(28)
        self.font_btn   = get_font(24, bold=True)

    def handle_event(self, event, game_state) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            
            # Back button
            back_rect = pygame.Rect(40, 40, 160, 45)
            if back_rect.collidepoint(mx, my):
                game_state.go_to(STATE_MAIN_MENU)
                return True
                
            # English button
            en_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, 250, 400, 60)
            if en_rect.collidepoint(mx, my):
                set_language(LANG_EN)
                return True
                
            # French button
            fr_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, 330, 400, 60)
            if fr_rect.collidepoint(mx, my):
                set_language(LANG_FR)
                return True
                
        return False

    def update(self, dt):
        pass

    def draw(self, surface):
        surface.fill(DARK_BG)
        mx, my = pygame.mouse.get_pos()
        
        # Title
        draw_text(surface, t("settings.title"), SCREEN_WIDTH // 2, 80,
                  self.font_title, GOLD, center=True)
        
        # Back button
        back_rect = pygame.Rect(40, 40, 160, 45)
        draw_button(surface, back_rect, t("settings.back"), self.font_btn, 
                    color=PANEL_BG, hover_color=CARD_HOVER, border_color=CARD_BORDER, 
                    mouse_pos=(mx, my))
        
        # Language selection
        draw_text(surface, t("settings.language"), SCREEN_WIDTH // 2, 200,
                  self.font_label, LIGHT_GREY, center=True)
        
        # Button rectangles
        en_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, 250, 400, 60)
        fr_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, 330, 400, 60)
        
        # Draw buttons with active state highlight
        from src.localization import get_language
        current_lang = get_language()
        
        draw_button(surface, en_rect, t("settings.lang_en"), self.font_btn,
                    color=(60, 60, 80) if current_lang == LANG_EN else PANEL_BG,
                    hover_color=CARD_HOVER,
                    border_color=GOLD if current_lang == LANG_EN else CARD_BORDER,
                    mouse_pos=(mx, my))
                    
        draw_button(surface, fr_rect, t("settings.lang_fr"), self.font_btn,
                    color=(60, 60, 80) if current_lang == LANG_FR else PANEL_BG,
                    hover_color=CARD_HOVER,
                    border_color=GOLD if current_lang == LANG_FR else CARD_BORDER,
                    mouse_pos=(mx, my))
