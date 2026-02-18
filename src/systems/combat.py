"""
Combat system — manages the turn loop between hero and enemies.
"""
from __future__ import annotations
from enum import Enum, auto
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.hero import Hero
    from src.models.enemy import Enemy
    from src.models.card import Card


class CombatPhase(Enum):
    PLAYER_TURN = auto()
    ENEMY_TURN  = auto()
    COMBAT_WON  = auto()
    COMBAT_LOST = auto()


class CombatState:
    def __init__(self, hero: "Hero", enemies: list["Enemy"]):
        self.hero = hero
        self.enemies = enemies
        self.phase = CombatPhase.PLAYER_TURN
        self.turn_number = 0
        self.log: list[str] = []
        self.selected_card: Optional["Card"] = None
        self.gold_reward = 0
        self._started = False

    # ── Setup ────────────────────────────────────────────────────────────────

    def start_combat(self):
        if self._started:
            return
        self._started = True
        self.hero.combat_state = self
        self.hero.prepare_deck()
        # Relic: on_combat_start
        self.hero.trigger_relics("on_combat_start")
        self._begin_player_turn()

    def _begin_player_turn(self):
        self.turn_number += 1
        self.phase = CombatPhase.PLAYER_TURN
        msgs = self.hero.start_of_turn()
        self._log(msgs)
        self._check_death()

    # ── Player Actions ────────────────────────────────────────────────────────

    def can_play_card(self, card: "Card") -> bool:
        if self.phase != CombatPhase.PLAYER_TURN:
            return False
        cost = card.cost
        if cost < 0:  # Unplayable (Wound) or special (Whirlwind uses all energy)
            if card.name == "Whirlwind":
                return self.hero.energy > 0
            return False
        if self.hero.corruption and card.card_type == "Skill":
            cost = 0
        return self.hero.energy >= cost

    def play_card(self, card: "Card", target: Optional["Enemy"] = None) -> list[str]:
        """Play a card from the hero's hand. Returns log messages."""
        if not self.can_play_card(card):
            return []
        if card not in self.hero.hand:
            return []

        msgs = []
        cost = card.cost
        if cost < 0:
            cost = 0  # Whirlwind handled inside effect
        if self.hero.corruption and card.card_type == "Skill":
            cost = 0

        self.hero.energy -= cost
        self.hero.hand.remove(card)

        # Notify relics
        for relic in self.hero.relics:
            relic.on_card_played(self.hero, card)

        # Execute card effect
        living_enemies = [e for e in self.enemies if not e.is_dead()]
        card.play(self.hero, target, living_enemies)

        msgs.append(f"Played: {card.name}")

        # Corruption: exhaust skills
        if self.hero.corruption and card.card_type == "Skill":
            self.hero.exhaust_pile.append(card)
        elif card.exhausts:
            self.hero.exhaust_pile.append(card)
        else:
            self.hero.discard_pile.append(card)

        # Juggernaut: if hero gained block, deal damage to random enemy
        if hasattr(self.hero, "_juggernaut_trigger") and self.hero._juggernaut_trigger > 0:
            if living_enemies:
                import random
                e = random.choice(living_enemies)
                e.take_damage(5, attacker=self.hero)
                msgs.append(f"Juggernaut deals 5 damage to {e.name}!")
            self.hero._juggernaut_trigger = 0

        self._check_death()
        return msgs

    def end_player_turn(self) -> list[str]:
        if self.phase != CombatPhase.PLAYER_TURN:
            return []
        msgs = self.hero.end_of_turn()
        self._log(msgs)
        self.phase = CombatPhase.ENEMY_TURN
        return msgs

    # ── Enemy Turn ────────────────────────────────────────────────────────────

    def execute_enemy_turn(self) -> list[str]:
        """Execute all enemy actions. Call after end_player_turn."""
        if self.phase != CombatPhase.ENEMY_TURN:
            return []
        msgs = []
        for enemy in self.enemies:
            if enemy.is_dead():
                continue
            msgs.extend(enemy.start_of_turn())
            msgs.extend(enemy.execute_action(self.hero))
            if self.hero.is_dead():
                break

        self._check_death()
        if self.phase not in (CombatPhase.COMBAT_WON, CombatPhase.COMBAT_LOST):
            self._begin_player_turn()
        self._log(msgs)
        return msgs

    # ── End / Rewards ─────────────────────────────────────────────────────────

    def _check_death(self):
        if self.hero.is_dead():
            self.phase = CombatPhase.COMBAT_LOST
            return
        living = [e for e in self.enemies if not e.is_dead()]
        if not living:
            self.phase = CombatPhase.COMBAT_WON
            self._on_combat_won()

    def _on_combat_won(self):
        import random
        is_boss = any(e.is_boss for e in self.enemies)
        base_gold = 20 if not is_boss else 80
        self.gold_reward = random.randint(base_gold, base_gold + 20)
        self.hero.gold += self.gold_reward
        self.hero.kills += 1
        # Relic: on_combat_end
        for relic in self.hero.relics:
            relic.on_combat_end(self.hero)

    def _log(self, msgs: list[str]):
        self.log.extend(msgs)
        if len(self.log) > 50:
            self.log = self.log[-50:]

    @property
    def is_over(self) -> bool:
        return self.phase in (CombatPhase.COMBAT_WON, CombatPhase.COMBAT_LOST)

    @property
    def player_won(self) -> bool:
        return self.phase == CombatPhase.COMBAT_WON
