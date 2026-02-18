"""
Enemy model and enemy pool.
"""
from __future__ import annotations
import random
from typing import Optional
from src.models.status import StatusEffect, make_status


class Action:
    """Represents an enemy's intended action."""
    ATTACK  = "attack"
    DEFEND  = "defend"
    BUFF    = "buff"
    DEBUFF  = "debuff"

    def __init__(self, action_type: str, value: int = 0, status_name: str = "",
                 status_stacks: int = 0, description: str = ""):
        self.type = action_type
        self.value = value                 # Damage or block amount
        self.status_name = status_name
        self.status_stacks = status_stacks
        self.description = description or self._default_desc()

    def _default_desc(self) -> str:
        if self.type == Action.ATTACK:
            return f"Attack {self.value}"
        if self.type == Action.DEFEND:
            return f"Defend {self.value}"
        if self.type == Action.BUFF:
            return f"Buff ({self.status_name} {self.status_stacks})"
        if self.type == Action.DEBUFF:
            return f"Debuff ({self.status_name} {self.status_stacks})"
        return "???"


class Enemy:
    def __init__(self, name: str, max_hp: int, action_pattern: list[Action],
                 tier: int = 1, is_boss: bool = False):
        self.name = name
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.block = 0
        self.statuses: list[StatusEffect] = []
        self.action_pattern = action_pattern
        self.action_index = 0
        self.tier = tier
        self.is_boss = is_boss
        self.next_action: Optional[Action] = action_pattern[0] if action_pattern else None

    def take_damage(self, amount: int, ignore_block: bool = False, attacker=None):
        if amount <= 0:
            return
        # Vulnerable modifier
        vuln = self._get_status("Vulnerable")
        if vuln and not ignore_block:
            amount = int(amount * 1.5)

        # Thorns
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

    def gain_block(self, amount: int):
        self.block = max(0, self.block + amount)

    def reset_block(self):
        self.block = 0

    def is_dead(self) -> bool:
        return self.current_hp <= 0

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

    def calc_damage(self, base: int) -> int:
        dmg = base
        strength = self._get_status("Strength")
        if strength:
            dmg += strength.stacks
        weak = self._get_status("Weak")
        if weak:
            dmg = int(dmg * 0.75)
        return max(0, dmg)

    def advance_action(self):
        self.action_index = (self.action_index + 1) % len(self.action_pattern)
        self.next_action = self.action_pattern[self.action_index]

    def execute_action(self, hero) -> list[str]:
        """Execute current action against the hero. Returns log messages."""
        messages = []
        action = self.next_action
        if action is None:
            return messages

        if action.type == Action.ATTACK:
            dmg = self.calc_damage(action.value)
            # Apply hero's Vulnerable
            vuln = hero._get_status("Vulnerable")
            if vuln:
                dmg = int(dmg * 1.5)
            hero.take_damage(dmg, attacker=self)
            messages.append(f"{self.name} attacks for {dmg} damage!")

        elif action.type == Action.DEFEND:
            self.gain_block(action.value)
            messages.append(f"{self.name} gains {action.value} Block.")

        elif action.type == Action.BUFF:
            if action.status_name:
                self.apply_status(make_status(action.status_name, action.status_stacks))
            messages.append(f"{self.name} buffs itself! ({action.description})")

        elif action.type == Action.DEBUFF:
            if action.status_name:
                hero.apply_status(make_status(action.status_name, action.status_stacks))
            messages.append(f"{self.name} debuffs you! ({action.description})")

        self.advance_action()
        return messages

    def start_of_turn(self) -> list[str]:
        self.reset_block()
        return self.tick_statuses()

    def scale(self, hp_mult: float, dmg_mult: float):
        """Scale this enemy's stats for difficulty."""
        self.max_hp = max(1, int(self.max_hp * hp_mult))
        self.current_hp = self.max_hp
        for action in self.action_pattern:
            if action.type == Action.ATTACK:
                action.value = max(1, int(action.value * dmg_mult))
        if self.next_action and self.next_action.type == Action.ATTACK:
            self.next_action.value = self.action_pattern[0].value


# ─────────────────────────────────────────────
# Enemy Definitions
# ─────────────────────────────────────────────

def _atk(dmg, desc="") -> Action:
    return Action(Action.ATTACK, dmg, description=desc or f"Attack {dmg}")

def _def(block, desc="") -> Action:
    return Action(Action.DEFEND, block, description=desc or f"Defend {block}")

def _buff(name, stacks, desc="") -> Action:
    return Action(Action.BUFF, status_name=name, status_stacks=stacks,
                  description=desc or f"{name} +{stacks}")

def _debuff(name, stacks, desc="") -> Action:
    return Action(Action.DEBUFF, status_name=name, status_stacks=stacks,
                  description=desc or f"{name} +{stacks}")


# Tier 1 enemies (floors 1-3)
TIER1_ENEMIES = [
    lambda: Enemy("Cultist", 48, [
        _buff("Ritual", 1, "Ritual +1"),
        _atk(6),
        _atk(6),
    ], tier=1),

    lambda: Enemy("Jaw Worm", 42, [
        _atk(11),
        _def(6),
        _atk(7),
        _def(6),
    ], tier=1),

    lambda: Enemy("Louse", 10, [
        _atk(5),
        _atk(7),
        _debuff("Weak", 1),
        _atk(5),
    ], tier=1),

    lambda: Enemy("Fungal Spore", 22, [
        _atk(6),
        _debuff("Vulnerable", 1),
        _atk(6),
        _debuff("Weak", 1),
    ], tier=1),

    lambda: Enemy("Slime", 35, [
        _atk(5),
        _atk(5),
        _def(8),
    ], tier=1),
]

# Tier 2 enemies (floors 4-6)
TIER2_ENEMIES = [
    lambda: Enemy("Gremlin Nob", 82, [
        _buff("Strength", 3, "Enrage +3 Str"),
        _atk(14),
        _atk(16),
        _debuff("Vulnerable", 2),
    ], tier=2),

    lambda: Enemy("Lagavulin", 112, [
        _def(8),
        _def(8),
        _debuff("Strength", -1, "Siphon Soul -1 Str"),
        _debuff("Dexterity", -1, "Siphon Soul -1 Dex"),
        _atk(18),
    ], tier=2),

    lambda: Enemy("Sentry", 38, [
        _atk(9),
        _debuff("Burn", 2, "Beam +2 Burn"),
        _atk(9),
        _debuff("Burn", 2, "Beam +2 Burn"),
    ], tier=2),

    lambda: Enemy("Blue Slaver", 46, [
        _atk(12),
        _debuff("Weak", 1),
        _atk(12),
    ], tier=2),

    lambda: Enemy("Red Slaver", 46, [
        _atk(13),
        _debuff("Vulnerable", 1),
        _atk(13),
    ], tier=2),
]

# Tier 3 enemies (floors 7+)
TIER3_ENEMIES = [
    lambda: Enemy("Writhing Mass", 160, [
        _atk(15),
        _debuff("Vulnerable", 2),
        _atk(20),
        _buff("Strength", 2),
    ], tier=3),

    lambda: Enemy("Repulsor", 29, [
        _atk(8),
        _atk(8),
        _debuff("Weak", 2),
        _debuff("Vulnerable", 2),
    ], tier=3),

    lambda: Enemy("Nemesis", 185, [
        _atk(45),
        _debuff("Burn", 3),
        _atk(45),
        _buff("Strength", 3),
    ], tier=3),

    lambda: Enemy("Deca", 265, [
        _buff("Strength", 4),
        _atk(30),
        _atk(30),
        _def(20),
    ], tier=3),
]

# Bosses (every 5 floors)
BOSSES = [
    # Floor 5 boss
    lambda: Enemy("The Guardian", 240, [
        _atk(32),
        _def(20),
        _atk(32),
        _buff("Strength", 3, "Defensive Mode"),
        _atk(32),
    ], tier=4, is_boss=True),

    # Floor 10 boss
    lambda: Enemy("Hexaghost", 250, [
        _atk(6),
        _atk(6),
        _debuff("Burn", 3),
        _atk(20),
        _buff("Strength", 2),
        _atk(20),
    ], tier=4, is_boss=True),

    # Floor 15 boss
    lambda: Enemy("Slime Boss", 140, [
        _atk(35),
        _debuff("Vulnerable", 3),
        _atk(35),
        _buff("Strength", 4, "Corrosive Slime"),
    ], tier=4, is_boss=True),

    # Floor 20+ boss (repeating)
    lambda: Enemy("Time Eater", 456, [
        _atk(32),
        _atk(32),
        _buff("Strength", 4, "Reverberate"),
        _debuff("Vulnerable", 2),
        _atk(32),
    ], tier=4, is_boss=True),
]


def get_enemy_for_floor(floor: int) -> Enemy:
    """Return a scaled enemy appropriate for the given floor."""
    from src.constants import enemy_hp_scale, enemy_dmg_scale, BOSS_EVERY

    if floor == 1:
        # Guarantee Slime for the first fight as requested
        enemy = Enemy("Slime", 35, [
            _atk(5),
            _atk(5),
            _def(8),
        ], tier=1)
    elif floor % BOSS_EVERY == 0:
        boss_index = (floor // BOSS_EVERY - 1) % len(BOSSES)
        enemy = BOSSES[boss_index]()
    elif floor <= 3:
        enemy = random.choice(TIER1_ENEMIES)()
    elif floor <= 6:
        enemy = random.choice(TIER2_ENEMIES)()
    else:
        enemy = random.choice(TIER3_ENEMIES)()

    enemy.scale(enemy_hp_scale(floor), enemy_dmg_scale(floor))
    return enemy


def get_elite_for_floor(floor: int) -> Enemy:
    """Return a scaled elite enemy."""
    from src.constants import enemy_hp_scale, enemy_dmg_scale
    if floor <= 5:
        pool = TIER2_ENEMIES
    else:
        pool = TIER3_ENEMIES
    enemy = random.choice(pool)()
    # Elites are stronger
    enemy.scale(enemy_hp_scale(floor) * 1.3, enemy_dmg_scale(floor) * 1.2)
    return enemy
