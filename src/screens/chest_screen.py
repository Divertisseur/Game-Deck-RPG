"""
Chest Screen — show chest reward (gold + optional relic).
"""
import pygame
from src.constants import *
from src.screens.ui_utils import draw_text, draw_button, draw_panel, get_font
from src.localization import t


class ChestScreen:
    def __init__(self):
        self.font_title = get_font(36, bold=True)
        self.font       = get_font(22)
        self.font_small = get_font(16)
        self.font_btn   = get_font(22, bold=True)

    def handle_event(self, event, game_state) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            take_rect  = pygame.Rect(SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 + 80, 240, 50)
            leave_rect = pygame.Rect(SCREEN_WIDTH // 2 - 80,  SCREEN_HEIGHT // 2 + 145, 160, 45)
            if take_rect.collidepoint(mx, my):
                game_state.complete_chest(take_relic=True)
                return True
            if leave_rect.collidepoint(mx, my):
                game_state.complete_chest(take_relic=False)
                return True
        return False

    def update(self, dt):
        pass

    def draw(self, surface, game_state):
        surface.fill(DARK_BG)
        reward = game_state.chest_reward
        mx, my = pygame.mouse.get_pos()

        draw_text(surface, t("chest.title"), SCREEN_WIDTH // 2, 60,
                  self.font_title, GOLD, center=True)

        # Panel
        px, py, pw, ph = SCREEN_WIDTH // 2 - 200, 130, 400, 280
        draw_panel(surface, px, py, pw, ph)

        if reward:
            draw_text(surface, f"{t('chest.gold')}{reward['gold']}", SCREEN_WIDTH // 2, py + 40,
                      self.font, GOLD, center=True)
            draw_text(surface, t("chest.found_relic"), SCREEN_WIDTH // 2, py + 90,
                      self.font_small, LIGHT_GREY, center=True)
            relic = reward.get("relic")
            if relic:
                pygame.draw.rect(surface, PURPLE,
                                 (SCREEN_WIDTH // 2 - 150, py + 115, 300, 60), border_radius=8)
                pygame.draw.rect(surface, (200, 150, 255),
                                 (SCREEN_WIDTH // 2 - 150, py + 115, 300, 60), 2, border_radius=8)
                draw_text(surface, t("relic.name." + relic.name), SCREEN_WIDTH // 2, py + 135,
                          self.font, WHITE, center=True)
                draw_text(surface, t("relic.desc." + relic.name), SCREEN_WIDTH // 2, py + 158,
                          self.font_small, LIGHT_GREY, center=True)

        # Buttons
        take_rect  = pygame.Rect(SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 + 80, 240, 50)
        leave_rect = pygame.Rect(SCREEN_WIDTH // 2 - 80,  SCREEN_HEIGHT // 2 + 145, 160, 45)
        draw_button(surface, take_rect, t("chest.take_both"), self.font_btn,
                    color=(40, 80, 40), hover_color=(60, 120, 60),
                    border_color=GREEN, mouse_pos=(mx, my))
        draw_button(surface, leave_rect, t("chest.take_gold"), self.font_small,
                    color=(30, 30, 50), hover_color=(50, 50, 90),
                    border_color=BLUE, mouse_pos=(mx, my))
