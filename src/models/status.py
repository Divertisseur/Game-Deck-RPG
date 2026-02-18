"""
Status Effects System
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.hero import Hero
    from src.models.enemy import Enemy


@dataclass
class StatusEffect:
    name: str
    stacks: int
    color: tuple = (200, 200, 200)
    description: str = ""

    def tick(self, target) -> list[str]:
        """Called at the start of the target's turn. Returns log messages."""
        return []

    def on_attack(self, base_damage: int, attacker) -> int:
        """Modify outgoing damage."""
        return base_damage

    def on_receive_damage(self, base_damage: int, target) -> int:
        """Modify incoming damage."""
        return base_damage

    def is_expired(self) -> bool:
        return self.stacks <= 0

    def __repr__(self):
        return f"{self.name}({self.stacks})"


class Strength(StatusEffect):
    def __init__(self, stacks: int):
        super().__init__("Strength", stacks, (220, 80, 80),
                         "Increases attack damage by 1 per stack.")

    def on_attack(self, base_damage: int, attacker) -> int:
        return base_damage + self.stacks


class Dexterity(StatusEffect):
    def __init__(self, stacks: int):
        super().__init__("Dexterity", stacks, (80, 140, 220),
                         "Increases block gained by 1 per stack.")


class Weak(StatusEffect):
    def __init__(self, stacks: int):
        super().__init__("Weak", stacks, (180, 180, 60),
                         "Reduces attack damage by 25%.")

    def on_attack(self, base_damage: int, attacker) -> int:
        return int(base_damage * 0.75)

    def tick(self, target) -> list[str]:
        self.stacks -= 1
        return []


class Vulnerable(StatusEffect):
    def __init__(self, stacks: int):
        super().__init__("Vulnerable", stacks, (220, 120, 60),
                         "Increases damage taken by 50%.")

    def on_receive_damage(self, base_damage: int, target) -> int:
        return int(base_damage * 1.5)

    def tick(self, target) -> list[str]:
        self.stacks -= 1
        return []


class Burn(StatusEffect):
    def __init__(self, stacks: int):
        super().__init__("Burn", stacks, (255, 140, 30),
                         "At end of turn, take stacks damage.")

    def tick(self, target) -> list[str]:
        dmg = self.stacks
        target.take_damage(dmg, ignore_block=True)
        return [f"{target.name} burns for {dmg} damage!"]


class Poison(StatusEffect):
    def __init__(self, stacks: int):
        super().__init__("Poison", stacks, (100, 220, 80),
                         "At start of turn, take stacks damage, then reduce by 1.")

    def tick(self, target) -> list[str]:
        dmg = self.stacks
        target.take_damage(dmg, ignore_block=True)
        self.stacks -= 1
        return [f"{target.name} is poisoned for {dmg} damage!"]


class Regeneration(StatusEffect):
    def __init__(self, stacks: int):
        super().__init__("Regeneration", stacks, (60, 220, 140),
                         "At start of turn, heal stacks HP, then reduce by 1.")

    def tick(self, target) -> list[str]:
        heal = self.stacks
        target.heal(heal)
        self.stacks -= 1
        return [f"{target.name} regenerates {heal} HP!"]


class Ritual(StatusEffect):
    """Enemy-specific: gains strength each turn."""
    def __init__(self, stacks: int):
        super().__init__("Ritual", stacks, (200, 60, 200),
                         "Gains stacks Strength at end of turn.")

    def tick(self, target) -> list[str]:
        target.apply_status(Strength(self.stacks))
        return [f"{target.name} performs a ritual, gaining {self.stacks} Strength!"]


class Thorns(StatusEffect):
    def __init__(self, stacks: int):
        super().__init__("Thorns", stacks, (180, 60, 60),
                         "When attacked, deals stacks damage back to attacker.")


STATUS_CLASSES = {
    "Strength": Strength,
    "Dexterity": Dexterity,
    "Weak": Weak,
    "Vulnerable": Vulnerable,
    "Burn": Burn,
    "Poison": Poison,
    "Regeneration": Regeneration,
    "Ritual": Ritual,
    "Thorns": Thorns,
}


def make_status(name: str, stacks: int) -> StatusEffect:
    cls = STATUS_CLASSES.get(name)
    if cls is None:
        raise ValueError(f"Unknown status: {name}")
    return cls(stacks)
