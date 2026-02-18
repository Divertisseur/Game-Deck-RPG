"""
Hero model.
"""
from __future__ import annotations
import random
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.card import Card
    from src.models.relic import Relic

from src.models.status import StatusEffect, Strength, Dexterity


class Hero:
    def __init__(self):
        self.name = "Iron Clad"
        self.max_hp = 80
        self.current_hp = 80
        self.block = 0
        self.energy = 3
        self.max_energy = 3
        self.gold = 99
        self.combat_state = None  # Reference for relic triggers

        # Deck management
        self.deck: list[Card] = []       # Full deck (all owned cards)
        self.draw_pile: list[Card] = []  # Cards to draw from
        self.hand: list[Card] = []       # Cards in hand
        self.discard_pile: list[Card] = []
        self.exhaust_pile: list[Card] = []

        # Statuses
        self.statuses: list[StatusEffect] = []

        # Relics
        self.relics: list[Relic] = []

        # Power flags
        self.barricade = False
        self.juggernaut = False
        self.corruption = False
        self.dark_embrace = False
        self.feel_no_pain = False
        self.evolve = False
        self.brutality = False
        self.berserk = False
        self.metallicize = 0
        self.combust = 0
        self._battle_trance_active = False

        # Stats tracking
        self.floor = 0
        self.kills = 0

    # ── HP ──────────────────────────────────────────────────────────────────

    def take_damage(self, amount: int, ignore_block: bool = False, attacker=None):
        if amount <= 0:
            return
        # Thorns retaliation
        if attacker and not ignore_block:
            thorns = self._get_status("Thorns")
            if thorns:
                attacker.take_damage(thorns.stacks, ignore_block=True)

        if not ignore_block:
            absorbed = min(self.block, amount)
            self.block -= absorbed
            amount -= absorbed
        if amount > 0:
            self.current_hp = max(0, self.current_hp - amount)

    def heal(self, amount: int):
        self.current_hp = min(self.max_hp, self.current_hp + amount)

    def is_dead(self) -> bool:
        return self.current_hp <= 0

    # ── Block ────────────────────────────────────────────────────────────────

    def gain_block(self, amount: int):
        amount = max(0, amount)
        self.block += amount
        # Juggernaut: deal damage to random enemy when gaining block
        if self.juggernaut and amount > 0:
            self._juggernaut_trigger = amount  # handled by combat system

    def reset_block(self):
        if not self.barricade:
            self.block = 0

    # ── Energy ───────────────────────────────────────────────────────────────

    def restore_energy(self):
        self.energy = self.max_energy
        if self.berserk:
            self.energy += 1

    # ── Damage Calculation ───────────────────────────────────────────────────

    def calc_damage(self, base: int) -> int:
        dmg = base + self.get_strength()
        # Apply Weak status
        weak = self._get_status("Weak")
        if weak:
            dmg = int(dmg * 0.75)
        return max(0, dmg)

    def get_strength(self) -> int:
        s = self._get_status("Strength")
        return s.stacks if s else 0

    def get_dexterity(self) -> int:
        d = self._get_status("Dexterity")
        return d.stacks if d else 0

    # ── Status Effects ────────────────────────────────────────────────────────

    def apply_status(self, status: StatusEffect):
        existing = self._get_status(status.name)
        if existing:
            existing.stacks += status.stacks
        else:
            self.statuses.append(status)

    def _get_status(self, name: str) -> Optional[StatusEffect]:
        for s in self.statuses:
            if s.name == name:
                return s
        return None

    def tick_statuses(self) -> list[str]:
        messages = []
        for s in list(self.statuses):
            messages.extend(s.tick(self))
        self.statuses = [s for s in self.statuses if not s.is_expired()]
        return messages

    def clear_combat_statuses(self):
        """Remove per-combat statuses (Weak, Vulnerable, etc.) after combat."""
        keep = {"Strength", "Dexterity"}
        self.statuses = [s for s in self.statuses if s.name in keep]

    # ── Card / Deck Management ────────────────────────────────────────────────

    def prepare_deck(self):
        """Shuffle deck into draw pile at start of combat."""
        self.draw_pile = [c.copy() for c in self.deck]
        random.shuffle(self.draw_pile)
        self.hand = []
        self.discard_pile = []
        self.exhaust_pile = []

    def draw_cards(self, n: int = 1):
        for _ in range(n):
            if not self.draw_pile:
                if not self.discard_pile:
                    return
                self.draw_pile = self.discard_pile[:]
                random.shuffle(self.draw_pile)
                self.discard_pile = []
            if self.draw_pile:
                card = self.draw_pile.pop()
                self.hand.append(card)

    def discard_hand(self):
        self.discard_pile.extend(self.hand)
        self.hand = []

    def exhaust_card(self, card: "Card"):
        if card in self.hand:
            self.hand.remove(card)
        self.exhaust_pile.append(card)
        if self.dark_embrace:
            self.draw_cards(1)
        if self.feel_no_pain:
            self.gain_block(3)

    def add_card_to_deck(self, card: "Card"):
        self.deck.append(card)

    def remove_card_from_deck(self, card: "Card"):
        for c in self.deck:
            if c.name == card.name:
                self.deck.remove(c)
                return True
        return False

    # ── Relics ────────────────────────────────────────────────────────────────

    def add_relic(self, relic: "Relic"):
        self.relics.append(relic)
        relic.on_obtain(self)

    def trigger_relics(self, event: str, **kwargs):
        for r in self.relics:
            getattr(r, event, lambda *a, **kw: None)(self, **kwargs)

    # ── Turn Hooks ────────────────────────────────────────────────────────────

    def start_of_turn(self) -> list[str]:
        messages = []
        self.reset_block()
        self.restore_energy()
        self._battle_trance_active = False
        self._juggernaut_trigger = 0

        # Brutality
        if self.brutality:
            self.take_damage(1, ignore_block=True)
            self.draw_cards(1)
            messages.append("Brutality: lost 1 HP, drew 1 card.")

        messages.extend(self.tick_statuses())
        self.draw_cards(5)
        self.trigger_relics("on_turn_start")
        return messages

    def end_of_turn(self) -> list[str]:
        messages = []
        # Metallicize
        if self.metallicize > 0:
            self.gain_block(self.metallicize)
            messages.append(f"Metallicize: gained {self.metallicize} Block.")
        # Combust
        if self.combust > 0:
            self.take_damage(self.combust, ignore_block=True)
            messages.append(f"Combust: lost {self.combust} HP.")
        self.discard_hand()
        return messages
