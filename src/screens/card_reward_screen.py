"""
Card Reward Screen — pick 1 of 3 cards after combat.
"""
import pygame
from src.constants import *
from src.screens.ui_utils import draw_text, draw_button, draw_panel, get_font, wrap_text
from src.models.card import ATTACK, SKILL, POWER
from src.localization import t

CARD_TYPE_COLORS = {ATTACK: ATTACK_COLOR, SKILL: SKILL_COLOR, POWER: POWER_COLOR}


class CardRewardScreen:
    def __init__(self):
        self.font_title = get_font(36, bold=True)
        self.font       = get_font(20)
        self.font_small = get_font(15)
        self.font_tiny  = get_font(13)
        self.font_btn   = get_font(22, bold=True)

    def handle_event(self, event, game_state) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            cards = game_state.card_reward_pool
            card_rects = self._card_rects(len(cards))
            for i, rect in enumerate(card_rects):
                if rect.collidepoint(mx, my) and i < len(cards):
                    game_state.pick_card_reward(cards[i])
                    return True
            # Skip button
            skip_rect = pygame.Rect(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT - 80, 160, 45)
            if skip_rect.collidepoint(mx, my):
                game_state.skip_card_reward()
                return True
        return False

    def _card_rects(self, n: int) -> list[pygame.Rect]:
        cw, ch = 200, 280
        spacing = 40
        total = n * cw + (n - 1) * spacing
        start_x = SCREEN_WIDTH // 2 - total // 2
        cy = SCREEN_HEIGHT // 2 - ch // 2 - 20
        return [pygame.Rect(start_x + i * (cw + spacing), cy, cw, ch) for i in range(n)]

    def update(self, dt):
        pass

    def draw(self, surface, game_state):
        surface.fill(DARK_BG)
        cards = game_state.card_reward_pool
        mx, my = pygame.mouse.get_pos()

        draw_text(surface, t("reward.title"), SCREEN_WIDTH // 2, 50,
                  self.font_title, GOLD, center=True)
        draw_text(surface, f"{t('reward.gold_earned')} +{game_state.combat_state.gold_reward if game_state.combat_state else 0}",
                  SCREEN_WIDTH // 2, 95, self.font, GREEN, center=True)

        card_rects = self._card_rects(len(cards))
        for i, (card, rect) in enumerate(zip(cards, card_rects)):
            hovered = rect.collidepoint(mx, my)
            border_col = CARD_TYPE_COLORS.get(card.card_type, CARD_BORDER)
            bg_col = CARD_HOVER if hovered else CARD_BG
            draw_panel(surface, rect.x, rect.y, rect.w, rect.h,
                       color=bg_col, border_color=border_col, radius=10)

            # Cost
            cost_text = str(card.cost) if card.cost >= 0 else "X"
            pygame.draw.circle(surface, ENERGY_COLOR, (rect.x + 20, rect.y + 20), 14)
            draw_text(surface, cost_text, rect.x + 20, rect.y + 20,
                      self.font, BLACK, center=True, shadow=False)

            # Rarity
            rarity_colors = {"Starter": GREY, "Common": WHITE, "Uncommon": (100, 180, 255), "Rare": GOLD}
            rc = rarity_colors.get(card.rarity, GREY)
            draw_text(surface, t("rarity." + card.rarity.lower()), rect.centerx, rect.y + 14,
                      self.font_tiny, rc, center=True)

            # Name
            draw_text(surface, t("card.name." + card.name), rect.centerx, rect.y + 50,
                      self.font, WHITE, center=True)

            # Type badge
            type_col = CARD_TYPE_COLORS.get(card.card_type, GREY)
            pygame.draw.rect(surface, type_col,
                             (rect.x + 10, rect.y + 75, rect.w - 20, 20), border_radius=4)
            draw_text(surface, t("card." + card.card_type.lower()), rect.centerx, rect.y + 85,
                      self.font_tiny, WHITE, center=True, shadow=False)

            # Description
            desc_text = t("card.desc." + card.name)
            lines = wrap_text(desc_text, self.font_small, rect.w - 20)
            for j, line in enumerate(lines[:6]):
                draw_text(surface, line, rect.centerx, rect.y + 110 + j * 22,
                          self.font_small, LIGHT_GREY, center=True, shadow=False)

            if hovered:
                draw_text(surface, t("reward.add_hint"),
                          rect.centerx, rect.bottom + 12, self.font_tiny, GOLD, center=True)

        # Skip button
        skip_rect = pygame.Rect(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT - 80, 160, 45)
        draw_button(surface, skip_rect, t("reward.skip"), self.font_btn,
                    color=(40, 30, 50), hover_color=(70, 50, 90),
                    border_color=GREY, mouse_pos=(mx, my))
