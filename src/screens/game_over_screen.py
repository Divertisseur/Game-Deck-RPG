"""
Game Over Screen — shown when the hero dies.
"""
import pygame
import math
from src.constants import *
from src.screens.ui_utils import draw_text, draw_button, draw_panel, get_font
from src.localization import t


class GameOverScreen:
    def __init__(self):
        self.font_title = get_font(64, bold=True)
        self.font       = get_font(26)
        self.font_small = get_font(18)
        self.font_btn   = get_font(26, bold=True)
        self.time = 0.0

    def handle_event(self, event, game_state) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            retry_rect = pygame.Rect(SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 + 100, 260, 55)
            menu_rect  = pygame.Rect(SCREEN_WIDTH // 2 - 90,  SCREEN_HEIGHT // 2 + 170, 180, 50)
            if retry_rect.collidepoint(mx, my):
                game_state.new_game()
                return True
            if menu_rect.collidepoint(mx, my):
                game_state.go_to(STATE_MAIN_MENU)
                return True
        return False

    def update(self, dt):
        self.time += dt

    def draw(self, surface, game_state):
        surface.fill((8, 5, 15))
        hero = game_state.hero
        mx, my = pygame.mouse.get_pos()

        # Red pulsing glow
        alpha = int(60 + 40 * math.sin(self.time * 1.5))
        glow = pygame.Surface((500, 200), pygame.SRCALPHA)
        pygame.draw.ellipse(glow, (180, 20, 20, alpha), (0, 0, 500, 200))
        surface.blit(glow, (SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 - 200))

        draw_text(surface, t("gameover.title"), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 160,
                  self.font_title, RED, center=True)

        # Stats panel
        draw_panel(surface, SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 80, 400, 160)
        draw_text(surface, f"{t('gameover.floor')} {game_state.dungeon.current_floor}",
                  SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 55, self.font, GOLD, center=True)
        draw_text(surface, f"{t('gameover.kills')} {hero.kills}",
                  SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 15, self.font, LIGHT_GREY, center=True)
        draw_text(surface, f"{t('gameover.deck')} {len(hero.deck)}",
                  SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 25, self.font_small, LIGHT_GREY, center=True)
        draw_text(surface, f"{t('gameover.relics')} {len(hero.relics)}",
                  SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 55, self.font_small, LIGHT_GREY, center=True)

        # Buttons
        retry_rect = pygame.Rect(SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 + 100, 260, 55)
        menu_rect  = pygame.Rect(SCREEN_WIDTH // 2 - 90,  SCREEN_HEIGHT // 2 + 170, 180, 50)
        draw_button(surface, retry_rect, t("gameover.new_run"), self.font_btn,
                    color=(60, 20, 20), hover_color=(100, 30, 30),
                    border_color=RED, mouse_pos=(mx, my))
        draw_button(surface, menu_rect, t("gameover.menu"), self.font,
                    color=(30, 25, 50), hover_color=(50, 40, 80),
                    border_color=PURPLE, mouse_pos=(mx, my))
