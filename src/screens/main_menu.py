"""
Main Menu Screen
"""
import pygame
import math
from src.constants import *
from src.screens.ui_utils import draw_text, draw_button, get_font
from src.localization import t


class MainMenuScreen:
    def __init__(self):
        self.font_title = get_font(72, bold=True)
        self.font_sub   = get_font(22)
        self.font_btn   = get_font(28, bold=True)
        self.time = 0
        self.particles = []
        self._init_particles()

    def _init_particles(self):
        import random
        for _ in range(60):
            self.particles.append({
                "x": random.randint(0, SCREEN_WIDTH),
                "y": random.randint(0, SCREEN_HEIGHT),
                "speed": random.uniform(0.2, 0.8),
                "size": random.randint(1, 3),
                "alpha": random.randint(50, 180),
            })

    def handle_event(self, event, game_state) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            btn_rect = pygame.Rect(SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2, 240, 55)
            settings_rect = pygame.Rect(SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 70, 240, 55)
            quit_rect = pygame.Rect(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 + 140, 160, 45)
            
            if btn_rect.collidepoint(mx, my):
                game_state.new_game()
                return True
            if settings_rect.collidepoint(mx, my):
                game_state.go_to(STATE_SETTINGS)
                return True
            if quit_rect.collidepoint(mx, my):
                pygame.quit()
                import sys; sys.exit()
        return False

    def update(self, dt):
        self.time += dt
        for p in self.particles:
            p["y"] -= p["speed"]
            if p["y"] < 0:
                import random
                p["y"] = SCREEN_HEIGHT
                p["x"] = random.randint(0, SCREEN_WIDTH)

    def draw(self, surface):
        # Background gradient
        surface.fill(DARK_BG)
        # Draw particles
        for p in self.particles:
            s = pygame.Surface((p["size"] * 2, p["size"] * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*PURPLE, p["alpha"]), (p["size"], p["size"]), p["size"])
            surface.blit(s, (int(p["x"]), int(p["y"])))

        # Animated glow behind title
        glow_alpha = int(120 + 60 * math.sin(self.time * 2))
        glow = pygame.Surface((600, 120), pygame.SRCALPHA)
        pygame.draw.ellipse(glow, (*PURPLE, glow_alpha), (0, 0, 600, 120))
        surface.blit(glow, (SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 - 180))

        # Title
        title_y = SCREEN_HEIGHT // 2 - 160
        draw_text(surface, t("menu.title_1"), SCREEN_WIDTH // 2 - 5, title_y,
                  self.font_title, GOLD, center=True)
        draw_text(surface, t("menu.title_2"), SCREEN_WIDTH // 2 - 5, title_y + 70,
                  self.font_title, (220, 100, 60), center=True)
        draw_text(surface, t("menu.title_3"), SCREEN_WIDTH // 2 - 5, title_y + 140,
                  self.font_title, PURPLE, center=True)

        draw_text(surface, t("menu.subtitle"),
                  SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30,
                  self.font_sub, LIGHT_GREY, center=True)

        mx, my = pygame.mouse.get_pos()
        # Start button
        btn_rect = pygame.Rect(SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2, 240, 55)
        draw_button(surface, btn_rect, t("menu.new_run"), self.font_btn,
                    color=(60, 40, 100), hover_color=(100, 60, 160),
                    border_color=PURPLE, mouse_pos=(mx, my))

        # Settings button
        settings_rect = pygame.Rect(SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 70, 240, 55)
        draw_button(surface, settings_rect, t("menu.settings"), self.font_btn,
                    color=(40, 40, 60), hover_color=(60, 60, 100),
                    border_color=BLUE, mouse_pos=(mx, my))

        # Quit button
        quit_rect = pygame.Rect(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 + 140, 160, 45)
        draw_button(surface, quit_rect, t("menu.quit"), self.font_sub,
                    color=(50, 30, 30), hover_color=(100, 40, 40),
                    border_color=DARK_RED, mouse_pos=(mx, my))

        # Version
        draw_text(surface, t("menu.version"), 10, SCREEN_HEIGHT - 24, get_font(16), GREY)
