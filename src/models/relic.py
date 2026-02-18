"""
Relic model and relic pool.
"""
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.hero import Hero


class Relic:
    def __init__(self, name: str, description: str, rarity: str = "Common"):
        self.name = name
        self.description = description
        self.rarity = rarity

    def on_obtain(self, hero: "Hero"):
        pass

    def on_combat_start(self, hero: "Hero"):
        pass

    def on_turn_start(self, hero: "Hero"):
        pass

    def on_turn_end(self, hero: "Hero"):
        pass

    def on_card_played(self, hero: "Hero", card):
        pass

    def on_damage_taken(self, hero: "Hero", amount: int) -> int:
        return amount

    def on_combat_end(self, hero: "Hero"):
        pass

    def __repr__(self):
        return f"Relic({self.name})"


# ─────────────────────────────────────────────
# Relic Definitions
# ─────────────────────────────────────────────

class BurningBlood(Relic):
    """Heal 6 HP at end of combat."""
    def __init__(self):
        super().__init__("Burning Blood", "Heal 6 HP at end of each combat.", "Starter")

    def on_combat_end(self, hero):
        hero.heal(6)


class Anchor(Relic):
    """Start each combat with 10 Block."""
    def __init__(self):
        super().__init__("Anchor", "Start each combat with 10 Block.", "Common")

    def on_combat_start(self, hero):
        hero.gain_block(10)


class BagOfPreparation(Relic):
    """Draw 2 extra cards on the first turn of combat."""
    def __init__(self):
        super().__init__("Bag of Preparation", "Draw 2 extra cards at the start of combat.", "Common")
        self._first_turn = False

    def on_combat_start(self, hero):
        self._first_turn = True

    def on_turn_start(self, hero):
        if self._first_turn:
            hero.draw_cards(2)
            self._first_turn = False


class RedSkull(Relic):
    """While at or below 50% HP, gain 3 Strength."""
    def __init__(self):
        super().__init__("Red Skull", "While at or below 50% HP, gain 3 Strength.", "Common")
        self._active = False

    def on_turn_start(self, hero):
        from src.models.status import make_status
        if hero.current_hp <= hero.max_hp // 2 and not self._active:
            hero.apply_status(make_status("Strength", 3))
            self._active = True
        elif hero.current_hp > hero.max_hp // 2 and self._active:
            # Remove the bonus (simplified)
            self._active = False


class Vajra(Relic):
    """Gain 1 Strength at the start of each combat."""
    def __init__(self):
        super().__init__("Vajra", "Gain 1 Strength at the start of each combat.", "Common")

    def on_combat_start(self, hero):
        from src.models.status import make_status
        hero.apply_status(make_status("Strength", 1))


class OddMushroom(Relic):
    """When you receive Weak, gain 3 Max HP."""
    def __init__(self):
        super().__init__("Odd Mushroom", "When Weakened, gain 3 Max HP.", "Common")


class Lantern(Relic):
    """Gain 1 extra Energy on the first turn of each combat."""
    def __init__(self):
        super().__init__("Lantern", "Gain 1 Energy on the first turn of combat.", "Common")
        self._first_turn = False

    def on_combat_start(self, hero):
        self._first_turn = True

    def on_turn_start(self, hero):
        if self._first_turn:
            hero.energy += 1
            self._first_turn = False


class TinyChest(Relic):
    """Every 4th room is a Chest."""
    def __init__(self):
        super().__init__("Tiny Chest", "Every 4th room is a Chest.", "Common")


class CoffeeDripper(Relic):
    """Gain 1 Energy each turn. You can no longer rest at campsites."""
    def __init__(self):
        super().__init__("Coffee Dripper", "Gain 1 Energy each turn.", "Rare")

    def on_turn_start(self, hero):
        hero.energy += 1


class PhilosophersStone(Relic):
    """Gain 1 Energy each turn. Enemies start with 1 Strength."""
    def __init__(self):
        super().__init__("Philosopher's Stone", "Gain 1 Energy each turn. Enemies gain 1 Strength.", "Rare")

    def on_turn_start(self, hero):
        hero.energy += 1


class Akabeko(Relic):
    """Your first Attack each combat deals 8 extra damage."""
    def __init__(self):
        super().__init__("Akabeko", "First Attack each combat deals 8 extra damage.", "Common")
        self._used = False

    def on_combat_start(self, hero):
        self._used = False

    def on_card_played(self, hero, card):
        from src.models.card import ATTACK
        if not self._used and card.card_type == ATTACK:
            # Bonus is applied via a temporary strength boost
            from src.models.status import make_status
            hero.apply_status(make_status("Strength", 8))
            self._used = True
            # Remove after one attack — handled by combat system tracking


class Centennial_Puzzle(Relic):
    """The first time you lose HP each combat, draw 3 cards."""
    def __init__(self):
        super().__init__("Centennial Puzzle", "First time you lose HP each combat, draw 3 cards.", "Common")
        self._triggered = False

    def on_combat_start(self, hero):
        self._triggered = False

    def on_damage_taken(self, hero, amount):
        if not self._triggered and amount > 0:
            hero.draw_cards(3)
            self._triggered = True
        return amount


class MagicFlower(Relic):
    """Healing is 50% more effective."""
    def __init__(self):
        super().__init__("Magic Flower", "Healing is 50% more effective.", "Rare")

    def on_obtain(self, hero):
        hero._healing_multiplier = 1.5


class Kryptonite(Relic):
    """On boss entry, deal 10% of boss max HP."""
    def __init__(self):
        super().__init__("Kryptonite", "Deal 10% Boss HP on entry.", "Uncommon")

    def on_combat_start(self, hero):
        from src.systems.combat import CombatState
        # Assuming we can check if any enemy is a boss
        for enemy in hero.combat_state.enemies:
            if getattr(enemy, 'is_boss', False):
                dmg = int(enemy.max_hp * 0.10)
                enemy.take_damage(dmg, ignore_block=True)


class FirePendant(Relic):
    """Heal 6 HP at end of combat."""
    def __init__(self):
        super().__init__("Fire Pendant", "Heal 6 HP at end of each combat.", "Starter")

    def on_combat_end(self, hero):
        hero.heal(6)


RELIC_POOL = [
    Anchor,
    BagOfPreparation,
    RedSkull,
    Vajra,
    OddMushroom,
    Lantern,
    TinyChest,
    CoffeeDripper,
    PhilosophersStone,
    Akabeko,
    Centennial_Puzzle,
    MagicFlower,
    Kryptonite,
    FirePendant,
]


def get_starter_relic() -> Relic:
    return FirePendant()


def get_random_relic(exclude_names: list[str] = None) -> Relic:
    import random
    exclude_names = exclude_names or []
    pool = [r for r in RELIC_POOL if r().name not in exclude_names]
    if not pool:
        pool = RELIC_POOL
    return random.choice(pool)()


def get_chest_reward() -> Relic:
    return get_random_relic()
