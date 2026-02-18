"""
Combat Screen — the main gameplay screen.
"""
import pygame
import math
from src.constants import *
from src.screens.ui_utils import (draw_text, draw_button, draw_panel, draw_bar,
                                   draw_status_icons, get_font, wrap_text)
from src.systems.combat import CombatPhase
from src.models.card import ATTACK, SKILL, POWER
from src.localization import t


CARD_TYPE_COLORS = {ATTACK: ATTACK_COLOR, SKILL: SKILL_COLOR, POWER: POWER_COLOR}


class CombatScreen:
    def __init__(self):
        self.font_title  = get_font(28, bold=True)
        self.font        = get_font(20)
        self.font_small  = get_font(15)
        self.font_tiny   = get_font(13)
        self.font_btn    = get_font(22, bold=True)
        self.font_card   = get_font(14, bold=True)
        self.font_card_s = get_font(12)

        self.hovered_card_idx = -1
        self.selected_card_idx = -1
        self.hovered_enemy_idx = -1
        self.log_messages: list[str] = []
        self.damage_numbers: list[dict] = []  # floating damage numbers
        self.time = 0.0
        self.enemy_turn_timer = 0.0
        self.enemy_turn_pending = False

    # ── Card Layout ────────────────────────────────────────────────────────────

    def _card_rects(self, hand_size: int) -> list[pygame.Rect]:
        rects = []
        total_w = hand_size * (CARD_W + 10) - 10
        start_x = SCREEN_WIDTH // 2 - total_w // 2
        for i in range(hand_size):
            x = start_x + i * (CARD_W + 10)
            y = CARD_HAND_Y
            rects.append(pygame.Rect(x, y, CARD_W, CARD_H))
        return rects

    def _enemy_rects(self, enemy_count: int) -> list[pygame.Rect]:
        rects = []
        ew, eh = 160, 180
        spacing = 20
        total = enemy_count * ew + (enemy_count - 1) * spacing
        start_x = SCREEN_WIDTH // 2 - total // 2
        for i in range(enemy_count):
            x = start_x + i * (ew + spacing)
            rects.append(pygame.Rect(x, 80, ew, eh))
        return rects

    # ── Events ────────────────────────────────────────────────────────────────

    def handle_event(self, event, game_state) -> bool:
        cs = game_state.combat_state
        if cs is None or cs.is_over:
            return False

        mx, my = pygame.mouse.get_pos()
        hero = cs.hero
        hand = hero.hand
        card_rects = self._card_rects(len(hand))
        enemy_rects = self._enemy_rects(len(cs.enemies))

        if event.type == pygame.MOUSEMOTION:
            self.hovered_card_idx = -1
            self.hovered_enemy_idx = -1
            for i, r in enumerate(card_rects):
                hover_r = r.inflate(0, 30)
                hover_r.y -= 30
                if hover_r.collidepoint(mx, my):
                    self.hovered_card_idx = i
            for i, r in enumerate(enemy_rects):
                if r.collidepoint(mx, my):
                    self.hovered_enemy_idx = i

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # End turn button
            end_rect = pygame.Rect(SCREEN_WIDTH - 160, SCREEN_HEIGHT - 80, 140, 50)
            if end_rect.collidepoint(mx, my) and cs.phase == CombatPhase.PLAYER_TURN:
                msgs = cs.end_player_turn()
                self._add_log(msgs)
                self.enemy_turn_pending = True
                self.enemy_turn_timer = 0.8
                self.selected_card_idx = -1
                return True

            # Card click
            for i, r in enumerate(card_rects):
                hover_r = r.inflate(0, 30)
                hover_r.y -= 30
                if hover_r.collidepoint(mx, my):
                    card = hand[i]
                    if not cs.can_play_card(card):
                        continue
                    if card.targeted:
                        # Select card, then click enemy
                        self.selected_card_idx = i
                    else:
                        msgs = cs.play_card(card, None)
                        self._add_log(msgs)
                        self.selected_card_idx = -1
                        self.hovered_card_idx = -1
                    return True

            # Enemy click (to target selected card)
            if self.selected_card_idx >= 0:
                for i, r in enumerate(enemy_rects):
                    if r.collidepoint(mx, my):
                        enemy = cs.enemies[i]
                        if not enemy.is_dead():
                            card = hand[self.selected_card_idx] if self.selected_card_idx < len(hand) else None
                            if card:
                                msgs = cs.play_card(card, enemy)
                                self._add_log(msgs)
                            self.selected_card_idx = -1
                        return True

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            self.selected_card_idx = -1

        return False

    def _add_log(self, msgs: list[str]):
        self.log_messages.extend(msgs)
        if len(self.log_messages) > 8:
            self.log_messages = self.log_messages[-8:]

    # ── Update ────────────────────────────────────────────────────────────────

    def update(self, dt, game_state):
        self.time += dt
        cs = game_state.combat_state
        if cs is None:
            return

        # Floating damage numbers
        for dn in self.damage_numbers[:]:
            dn["y"] -= 60 * dt
            dn["alpha"] -= 200 * dt
            if dn["alpha"] <= 0:
                self.damage_numbers.remove(dn)

        # Enemy turn delay
        if self.enemy_turn_pending:
            self.enemy_turn_timer -= dt
            if self.enemy_turn_timer <= 0:
                self.enemy_turn_pending = False
                msgs = cs.execute_enemy_turn()
                self._add_log(msgs)

        # Transition after combat ends
        if cs.is_over and not self.enemy_turn_pending:
            if cs.player_won:
                game_state.combat_won()
            else:
                game_state.game_over()

    # ── Draw ──────────────────────────────────────────────────────────────────

    def draw(self, surface, game_state):
        cs = game_state.combat_state
        if cs is None:
            return

        surface.fill(DARK_BG)
        hero = cs.hero
        enemies = cs.enemies
        mx, my = pygame.mouse.get_pos()

        # ── Background dungeon atmosphere ──
        self._draw_bg(surface)

        # ── Hero panel (bottom-left) ──
        self._draw_hero_panel(surface, hero)

        # ── Enemies ──
        enemy_rects = self._enemy_rects(len(enemies))
        for i, (enemy, rect) in enumerate(zip(enemies, enemy_rects)):
            self._draw_enemy(surface, enemy, rect, i, mx, my)

        # ── Hand ──
        hand = hero.hand
        card_rects = self._card_rects(len(hand))
        for i, (card, rect) in enumerate(zip(hand, card_rects)):
            hovered = (i == self.hovered_card_idx)
            selected = (i == self.selected_card_idx)
            self._draw_card(surface, card, rect, hovered, selected, cs.can_play_card(card))

        # ── Energy ──
        self._draw_energy(surface, hero)

        # ── Draw/Discard piles ──
        draw_text(surface, f"{t('combat.draw')} {len(hero.draw_pile)}", 20, SCREEN_HEIGHT - 30,
                  self.font_small, LIGHT_GREY)
        draw_text(surface, f"{t('combat.discard')} {len(hero.discard_pile)}",
                  SCREEN_WIDTH - 150, SCREEN_HEIGHT - 30, self.font_small, LIGHT_GREY)

        # ── End Turn button ──
        end_rect = pygame.Rect(SCREEN_WIDTH - 160, SCREEN_HEIGHT - 80, 140, 50)
        can_end = cs.phase == CombatPhase.PLAYER_TURN and not self.enemy_turn_pending
        btn_color = (40, 80, 40) if can_end else (50, 50, 50)
        btn_hover = (60, 120, 60) if can_end else (50, 50, 50)
        draw_button(surface, end_rect, t("combat.end_turn"), self.font_btn,
                    color=btn_color, hover_color=btn_hover,
                    border_color=GREEN if can_end else GREY, mouse_pos=(mx, my))

        # ── Turn indicator ──
        phase_text = t("combat.your_turn") if cs.phase == CombatPhase.PLAYER_TURN else t("combat.enemy_turn")
        phase_col  = GREEN if cs.phase == CombatPhase.PLAYER_TURN else RED
        draw_text(surface, phase_text, SCREEN_WIDTH // 2, 15,
                  self.font_btn, phase_col, center=True)

        # ── Combat log ──
        self._draw_log(surface)

        # ── Selected card indicator ──
        if self.selected_card_idx >= 0:
            draw_text(surface, t("combat.target_hint"),
                      SCREEN_WIDTH // 2, CARD_HAND_Y - 30,
                      self.font_small, GOLD, center=True)

    def _draw_bg(self, surface):
        # Subtle vignette
        for i in range(8):
            alpha = 15 + i * 5
            s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            pygame.draw.rect(s, (0, 0, 0, alpha),
                             (i * 20, i * 15, SCREEN_WIDTH - i * 40, SCREEN_HEIGHT - i * 30),
                             3)
            surface.blit(s, (0, 0))

    def _draw_hero_panel(self, surface, hero):
        draw_panel(surface, 10, SCREEN_HEIGHT - 200, 220, 120)
        draw_text(surface, hero.name, 20, SCREEN_HEIGHT - 195, self.font, WHITE)
        draw_bar(surface, 20, SCREEN_HEIGHT - 168, 180, 18,
                 hero.current_hp, hero.max_hp, HP_BAR_FG, HP_BAR_BG,
                 f"{t('hero.hp')} {hero.current_hp}/{hero.max_hp}")
        if hero.block > 0:
            draw_text(surface, f"🛡 {hero.block}", 20, SCREEN_HEIGHT - 142,
                      self.font, BLOCK_COLOR)
        draw_status_icons(surface, hero.statuses, 20, SCREEN_HEIGHT - 115, self.font_tiny)

    def _draw_enemy(self, surface, enemy, rect, idx, mx, my):
        if enemy.is_dead():
            # Draw faded dead enemy
            s = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
            pygame.draw.rect(s, (60, 20, 20, 80), (0, 0, rect.w, rect.h), border_radius=10)
            surface.blit(s, rect.topleft)
            draw_text(surface, "DEAD", rect.centerx, rect.centery,
                      self.font, RED, center=True)
            return

        hovered = rect.collidepoint(mx, my)
        border_col = RED if hovered else CARD_BORDER
        draw_panel(surface, rect.x, rect.y, rect.w, rect.h,
                   color=(35, 20, 20), border_color=border_col)

        # Enemy name
        draw_text(surface, t("enemy.name." + enemy.name), rect.centerx, rect.y + 8,
                  self.font_small, WHITE, center=True)

        # HP bar
        draw_bar(surface, rect.x + 10, rect.y + 30, rect.w - 20, 16,
                 enemy.current_hp, enemy.max_hp, HP_BAR_FG, HP_BAR_BG,
                 f"{enemy.current_hp}/{enemy.max_hp}")

        # Block
        if enemy.block > 0:
            draw_text(surface, f"🛡 {enemy.block}", rect.x + 10, rect.y + 52,
                      self.font_small, BLOCK_COLOR)

        # Intent
        if enemy.next_action:
            action = enemy.next_action
            intent_col = RED if action.type == "attack" else (BLUE if action.type == "defend" else PURPLE)
            intent_label = t("intent." + action.type)
            val_str = f" {action.value}" if action.value > 0 else ""
            draw_text(surface, f"{intent_label}{val_str}",
                      rect.x + 5, rect.y + 75, self.font_tiny, intent_col)

        # Statuses
        draw_status_icons(surface, enemy.statuses, rect.x + 5, rect.y + 100, self.font_tiny)

        # Enemy art (simple geometric shape)
        cx, cy = rect.centerx, rect.y + 145
        pulse = int(5 * math.sin(self.time * 3 + idx))
        pygame.draw.circle(surface, (180, 60, 60), (cx, cy), 18 + pulse)
        pygame.draw.circle(surface, (220, 100, 100), (cx, cy), 12 + pulse // 2)
        pygame.draw.circle(surface, (255, 150, 150), (cx, cy), 6)

    def _draw_card(self, surface, card, rect, hovered, selected, playable):
        draw_y = rect.y - (30 if hovered else 0)
        bg_col = CARD_HOVER if hovered else CARD_BG
        if selected:
            bg_col = (80, 60, 120)
        if not playable:
            bg_col = (25, 20, 35)

        border_col = CARD_TYPE_COLORS.get(card.card_type, CARD_BORDER)
        if not playable:
            border_col = (60, 55, 80)

        draw_panel(surface, rect.x, draw_y, CARD_W, CARD_H,
                   color=bg_col, border_color=border_col, radius=8)

        # Cost circle
        cost_col = ENERGY_COLOR if card.cost >= 0 else GREY
        cost_text = str(card.cost) if card.cost >= 0 else "X"
        pygame.draw.circle(surface, cost_col, (rect.x + 15, draw_y + 15), 12)
        draw_text(surface, cost_text, rect.x + 15, draw_y + 15,
                  self.font_card, BLACK, center=True, shadow=False)

        # Card type badge
        type_col = CARD_TYPE_COLORS.get(card.card_type, GREY)
        pygame.draw.rect(surface, type_col,
                         (rect.x + 5, draw_y + CARD_H - 28, CARD_W - 10, 18),
                         border_radius=4)
        draw_text(surface, t("card." + card.card_type.lower()), rect.centerx, draw_y + CARD_H - 19,
                  self.font_tiny, WHITE, center=True, shadow=False)

        # Name
        draw_text(surface, t("card.name." + card.name), rect.centerx, draw_y + 30,
                  self.font_card, WHITE, center=True)

        # Description (wrapped)
        desc_key = "card.desc." + card.name
        desc_text = t(desc_key)
        lines = wrap_text(desc_text, self.font_tiny, CARD_W - 14)
        for j, line in enumerate(lines[:4]):
            draw_text(surface, line, rect.centerx, draw_y + 55 + j * 18,
                      self.font_tiny, LIGHT_GREY, center=True, shadow=False)

        # Rarity dot
        rarity_colors = {"Starter": GREY, "Common": WHITE, "Uncommon": (100, 180, 255), "Rare": GOLD}
        rc = rarity_colors.get(card.rarity, GREY)
        pygame.draw.circle(surface, rc, (rect.x + CARD_W - 12, draw_y + 12), 5)

    def _draw_energy(self, surface, hero):
        cx, cy = 80, SCREEN_HEIGHT - 80
        pygame.draw.circle(surface, (60, 50, 20), (cx, cy), 30)
        pygame.draw.circle(surface, ENERGY_COLOR, (cx, cy), 28)
        pygame.draw.circle(surface, (255, 230, 100), (cx, cy), 22)
        draw_text(surface, str(hero.energy), cx, cy, self.font_title, BLACK, center=True, shadow=False)
        draw_text(surface, f"/{hero.max_energy}", cx + 18, cy + 10, self.font_tiny, (80, 60, 0), shadow=False)

    def _draw_log(self, surface):
        log_x = SCREEN_WIDTH - 320
        log_y = SCREEN_HEIGHT - 250
        draw_panel(surface, log_x, log_y, 300, 160, color=(15, 12, 25, 180))
        draw_text(surface, t("combat.log_title"), log_x + 10, log_y + 5, self.font_tiny, GREY)
        for i, msg in enumerate(self.log_messages[-7:]):
            alpha = 100 + int(155 * (i + 1) / 7)
            col = (alpha, alpha, alpha)
            draw_text(surface, msg[:38], log_x + 8, log_y + 22 + i * 19,
                      self.font_tiny, col, shadow=False)
