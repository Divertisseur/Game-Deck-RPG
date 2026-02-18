"""
Merchant Screen — buy cards, remove cards, buy relics.
"""
import pygame
from src.constants import *
from src.screens.ui_utils import draw_text, draw_button, draw_panel, draw_bar, get_font, wrap_text
from src.models.card import ATTACK, SKILL, POWER
from src.localization import t

CARD_TYPE_COLORS = {ATTACK: ATTACK_COLOR, SKILL: SKILL_COLOR, POWER: POWER_COLOR}


class MerchantScreen:
    def __init__(self):
        self.font_title = get_font(36, bold=True)
        self.font       = get_font(20)
        self.font_small = get_font(15)
        self.font_tiny  = get_font(13)
        self.font_btn   = get_font(22, bold=True)
        self.message = ""
        self.message_timer = 0.0

    def handle_event(self, event, game_state) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            hero = game_state.hero
            cards = game_state.merchant_cards

            # Card buy buttons
            for i, (card, price) in enumerate(cards):
                btn_rect = self._card_buy_rect(i)
                if btn_rect.collidepoint(mx, my):
                    if hero.gold >= price:
                        hero.gold -= price
                        hero.add_card_to_deck(card)
                        game_state.merchant_cards.pop(i)
                        self._show_msg(f"{t('merchant.bought')} {t('card.name.' + card.name)}!")
                    else:
                        self._show_msg(t('merchant.no_gold'))
                    return True

            # Remove card button
            remove_rect = pygame.Rect(SCREEN_WIDTH - 220, 200, 180, 45)
            if remove_rect.collidepoint(mx, my):
                from src.constants import REMOVE_PRICE
                if hero.gold >= REMOVE_PRICE and len(hero.deck) > 1:
                    import random
                    card = random.choice(hero.deck)
                    hero.remove_card_from_deck(card)
                    hero.gold -= REMOVE_PRICE
                    self._show_msg(f"{t('merchant.removed')} {t('card.name.' + card.name)}!")
                elif hero.gold < REMOVE_PRICE:
                    self._show_msg(t('merchant.no_gold'))
                else:
                    self._show_msg(t('merchant.deck_small'))
                return True

            # Leave button
            leave_rect = pygame.Rect(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT - 80, 160, 45)
            if leave_rect.collidepoint(mx, my):
                game_state.complete_merchant()
                return True
        return False

    def _card_buy_rect(self, i: int) -> pygame.Rect:
        cw = 180
        spacing = 20
        total = 5 * cw + 4 * spacing
        start_x = SCREEN_WIDTH // 2 - total // 2
        return pygame.Rect(start_x + i * (cw + spacing), 200, cw, 260)

    def _show_msg(self, msg: str):
        self.message = msg
        self.message_timer = 2.5

    def update(self, dt):
        if self.message_timer > 0:
            self.message_timer -= dt

    def draw(self, surface, game_state):
        surface.fill(DARK_BG)
        hero = game_state.hero
        cards = game_state.merchant_cards
        mx, my = pygame.mouse.get_pos()

        # Title
        draw_text(surface, t("merchant.title"), SCREEN_WIDTH // 2, 30,
                  self.font_title, GOLD, center=True)
        draw_text(surface, f"{t('merchant.gold')} {hero.gold}", SCREEN_WIDTH // 2, 75,
                  self.font, GOLD, center=True)

        # Cards for sale
        for i, (card, price) in enumerate(cards):
            rect = self._card_buy_rect(i)
            hovered = rect.collidepoint(mx, my)
            can_buy = hero.gold >= price
            border_col = CARD_TYPE_COLORS.get(card.card_type, CARD_BORDER)
            bg_col = CARD_HOVER if hovered else CARD_BG
            if not can_buy:
                bg_col = (20, 18, 28)
                border_col = (60, 55, 80)
            draw_panel(surface, rect.x, rect.y, rect.w, rect.h,
                       color=bg_col, border_color=border_col, radius=8)

            # Cost circle
            cost_text = str(card.cost) if card.cost >= 0 else "X"
            pygame.draw.circle(surface, ENERGY_COLOR, (rect.x + 18, rect.y + 18), 12)
            draw_text(surface, cost_text, rect.x + 18, rect.y + 18,
                      self.font_small, BLACK, center=True, shadow=False)

            draw_text(surface, t("card.name." + card.name), rect.centerx, rect.y + 40,
                      self.font_small, WHITE, center=True)

            type_col = CARD_TYPE_COLORS.get(card.card_type, GREY)
            pygame.draw.rect(surface, type_col,
                             (rect.x + 8, rect.y + 60, rect.w - 16, 18), border_radius=4)
            draw_text(surface, t("card." + card.card_type.lower()), rect.centerx, rect.y + 69,
                      self.font_tiny, WHITE, center=True, shadow=False)

            desc_text = t("card.desc." + card.name)
            lines = wrap_text(desc_text, self.font_tiny, rect.w - 16)
            for j, line in enumerate(lines[:5]):
                draw_text(surface, line, rect.centerx, rect.y + 90 + j * 18,
                          self.font_tiny, LIGHT_GREY, center=True, shadow=False)

            # Price tag
            price_col = GOLD if can_buy else RED
            pygame.draw.rect(surface, (40, 35, 10) if can_buy else (40, 10, 10),
                             (rect.x + 10, rect.bottom - 35, rect.w - 20, 28), border_radius=6)
            draw_text(surface, f"{price} {t('merchant.gold').lower().replace(':', '')}", rect.centerx, rect.bottom - 21,
                      self.font_small, price_col, center=True)

        # Remove card service
        remove_rect = pygame.Rect(SCREEN_WIDTH - 220, 200, 180, 45)
        can_remove = hero.gold >= REMOVE_PRICE
        draw_button(surface, remove_rect,
                    f"{t('merchant.remove')} ({REMOVE_PRICE}g)", self.font_tiny,
                    color=(50, 20, 20) if can_remove else (30, 25, 30),
                    hover_color=(90, 30, 30),
                    border_color=RED if can_remove else GREY,
                    mouse_pos=(mx, my))

        # Message
        if self.message_timer > 0:
            draw_text(surface, self.message, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 120,
                      self.font, GOLD, center=True)

        # Leave button
        leave_rect = pygame.Rect(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT - 80, 160, 45)
        draw_button(surface, leave_rect, t("merchant.leave"), self.font_btn,
                    color=(30, 30, 50), hover_color=(50, 50, 90),
                    border_color=BLUE, mouse_pos=(mx, my))
