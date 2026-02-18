"""
Event Screen — random dungeon events with multiple choices.
"""
import pygame
from src.constants import *
from src.screens.ui_utils import draw_text, draw_button, draw_panel, get_font, wrap_text
from src.localization import t


class EventScreen:
    def __init__(self):
        self.font_title = get_font(32, bold=True)
        self.font       = get_font(20)
        self.font_small = get_font(16)
        self.font_btn   = get_font(20, bold=True)
        self.result_msg = ""
        self.result_timer = 0.0
        self.choice_made = False

    def handle_event(self, event, game_state) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            ev = game_state.current_event
            if ev is None:
                return False

            if self.choice_made:
                # Continue button
                cont_rect = pygame.Rect(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT - 80, 160, 45)
                if cont_rect.collidepoint(mx, my):
                    self.choice_made = False
                    self.result_msg = ""
                    game_state.complete_event()
                return True

            for i, choice in enumerate(ev.choices):
                btn_rect = self._choice_rect(i)
                if btn_rect.collidepoint(mx, my):
                    result = choice.effect_fn(game_state.hero)
                    self.result_msg = str(result) if result else "Done."
                    self.choice_made = True
                    return True
        return False

    def _choice_rect(self, i: int) -> pygame.Rect:
        return pygame.Rect(SCREEN_WIDTH // 2 - 220, 340 + i * 65, 440, 50)

    def update(self, dt):
        pass

    def draw(self, surface, game_state):
        surface.fill(DARK_BG)
        ev = game_state.current_event
        if ev is None:
            return
        mx, my = pygame.mouse.get_pos()

        draw_text(surface, f"{t('event.title_prefix')}{t('event.name.' + ev.title)}", SCREEN_WIDTH // 2, 50,
                  self.font_title, GOLD, center=True)

        # Description panel
        draw_panel(surface, SCREEN_WIDTH // 2 - 300, 100, 600, 200)
        desc_text = t("event.desc." + ev.title)
        lines = wrap_text(desc_text, self.font, 560)
        for i, line in enumerate(lines):
            draw_text(surface, line, SCREEN_WIDTH // 2, 120 + i * 30,
                      self.font, LIGHT_GREY, center=True)

        if not self.choice_made:
            draw_text(surface, t("event.what_do"), SCREEN_WIDTH // 2, 315,
                      self.font_small, GREY, center=True)
            for i, choice in enumerate(ev.choices):
                btn_rect = self._choice_rect(i)
                choice_text = t(f"event.choice.{ev.title}.{i}")
                draw_button(surface, btn_rect, choice_text, self.font_btn,
                            color=(30, 25, 50), hover_color=(60, 50, 100),
                            border_color=PURPLE, mouse_pos=(mx, my))
        else:
            # Show result
            draw_panel(surface, SCREEN_WIDTH // 2 - 250, 340, 500, 80)
            draw_text(surface, self.result_msg, SCREEN_WIDTH // 2, 380,
                      self.font, GREEN, center=True)
            cont_rect = pygame.Rect(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT - 80, 160, 45)
            draw_button(surface, cont_rect, t("event.continue"), self.font_btn,
                        color=(30, 60, 30), hover_color=(50, 100, 50),
                        border_color=GREEN, mouse_pos=(mx, my))
