"""
Card model and full card pool.
"""
from __future__ import annotations
import random
from typing import TYPE_CHECKING, Callable, Optional

if TYPE_CHECKING:
    from src.models.hero import Hero
    from src.models.enemy import Enemy

# Card types
ATTACK = "Attack"
SKILL  = "Skill"
POWER  = "Power"

# Rarities
COMMON   = "Common"
UNCOMMON = "Uncommon"
RARE     = "Rare"
STARTER  = "Starter"


class Card:
    def __init__(
        self,
        name: str,
        cost: int,
        card_type: str,
        rarity: str,
        description: str,
        effect_fn: Callable,
        targeted: bool = True,
        exhausts: bool = False,
    ):
        self.name = name
        self.cost = cost
        self.card_type = card_type
        self.rarity = rarity
        self.description = description
        self.effect_fn = effect_fn
        self.targeted = targeted   # Does it need an enemy target?
        self.exhausts = exhausts   # Removed from deck after use

    def play(self, hero: "Hero", target: Optional["Enemy"] = None, enemies: list = None):
        """Execute this card's effect."""
        self.effect_fn(hero, target, enemies or [])

    def copy(self) -> "Card":
        return Card(
            self.name, self.cost, self.card_type, self.rarity,
            self.description, self.effect_fn, self.targeted, self.exhausts
        )

    def __repr__(self):
        return f"Card({self.name}, cost={self.cost})"


# ─────────────────────────────────────────────
# Helper imports (deferred to avoid circular)
# ─────────────────────────────────────────────
def _apply_status(target, name: str, stacks: int):
    from src.models.status import make_status
    target.apply_status(make_status(name, stacks))


# ─────────────────────────────────────────────
# Card Definitions
# ─────────────────────────────────────────────

def _strike(hero, target, enemies):
    dmg = hero.calc_damage(6)
    if target:
        target.take_damage(dmg, attacker=hero)

def _defend(hero, target, enemies):
    hero.gain_block(5 + hero.get_dexterity())

def _bash(hero, target, enemies):
    dmg = hero.calc_damage(8)
    if target:
        target.take_damage(dmg, attacker=hero)
        _apply_status(target, "Vulnerable", 2)

def _heavy_blade(hero, target, enemies):
    dmg = hero.calc_damage(14)
    if target:
        target.take_damage(dmg, attacker=hero)

def _twin_strike(hero, target, enemies):
    for _ in range(2):
        dmg = hero.calc_damage(5)
        if target:
            target.take_damage(dmg, attacker=hero)

def _body_slam(hero, target, enemies):
    dmg = hero.calc_damage(hero.block)
    if target:
        target.take_damage(dmg, attacker=hero)

def _pommel_strike(hero, target, enemies):
    dmg = hero.calc_damage(9)
    if target:
        target.take_damage(dmg, attacker=hero)
    hero.draw_cards(1)

def _iron_wave(hero, target, enemies):
    dmg = hero.calc_damage(5)
    if target:
        target.take_damage(dmg, attacker=hero)
    hero.gain_block(5 + hero.get_dexterity())

def _cleave(hero, target, enemies):
    dmg = hero.calc_damage(8)
    for e in enemies:
        e.take_damage(dmg, attacker=hero)

def _whirlwind(hero, target, enemies):
    for _ in range(hero.energy):
        dmg = hero.calc_damage(5)
        for e in enemies:
            e.take_damage(dmg, attacker=hero)
    hero.energy = 0

def _perfected_strike(hero, target, enemies):
    strikes = sum(1 for c in hero.deck + hero.hand + hero.discard_pile
                  if "strike" in c.name.lower())
    dmg = hero.calc_damage(6 + strikes * 2)
    if target:
        target.take_damage(dmg, attacker=hero)

def _sword_boomerang(hero, target, enemies):
    for _ in range(3):
        if enemies:
            e = random.choice(enemies)
            e.take_damage(hero.calc_damage(3), attacker=hero)

def _thunderclap(hero, target, enemies):
    dmg = hero.calc_damage(4)
    for e in enemies:
        e.take_damage(dmg, attacker=hero)
        _apply_status(e, "Vulnerable", 1)

def _headbutt(hero, target, enemies):
    dmg = hero.calc_damage(9)
    if target:
        target.take_damage(dmg, attacker=hero)
    if hero.discard_pile:
        card = random.choice(hero.discard_pile)
        hero.discard_pile.remove(card)
        hero.draw_pile.insert(0, card)

def _shrug_it_off(hero, target, enemies):
    hero.gain_block(8 + hero.get_dexterity())
    hero.draw_cards(1)

def _true_grit(hero, target, enemies):
    hero.gain_block(7 + hero.get_dexterity())
    if hero.hand:
        card = random.choice(hero.hand)
        hero.hand.remove(card)
        hero.exhaust_pile.append(card)

def _armaments(hero, target, enemies):
    hero.gain_block(5 + hero.get_dexterity())
    # Upgrade a random card in hand (simplified: give +1 damage description)
    hero.draw_cards(1)

def _battle_trance(hero, target, enemies):
    hero.draw_cards(3)
    # Can't draw more cards this turn — simplified: no further draw
    hero._battle_trance_active = True

def _bloodletting(hero, target, enemies):
    hero.take_damage(3, ignore_block=True)
    hero.energy += 2

def _second_wind(hero, target, enemies):
    non_attacks = [c for c in hero.hand if c.card_type != ATTACK]
    block_gained = 0
    for c in non_attacks:
        hero.hand.remove(c)
        hero.exhaust_pile.append(c)
        block_gained += 5
    hero.gain_block(block_gained)

def _entrench(hero, target, enemies):
    hero.gain_block(hero.block)

def _flame_barrier(hero, target, enemies):
    hero.gain_block(12 + hero.get_dexterity())
    _apply_status(hero, "Thorns", 4)

def _burning_pact(hero, target, enemies):
    if hero.hand:
        card = random.choice(hero.hand)
        hero.hand.remove(card)
        hero.exhaust_pile.append(card)
        hero.draw_cards(2)

def _offering(hero, target, enemies):
    hero.take_damage(6, ignore_block=True)
    hero.energy += 2
    hero.draw_cards(3)

def _inflame(hero, target, enemies):
    _apply_status(hero, "Strength", 2)

def _flex(hero, target, enemies):
    _apply_status(hero, "Strength", 2)
    # At end of turn lose 2 strength — simplified: just give strength

def _limit_break(hero, target, enemies):
    str_val = hero.get_strength()
    _apply_status(hero, "Strength", str_val)

def _spot_weakness(hero, target, enemies):
    if target and target.next_action and target.next_action.get("type") == "attack":
        _apply_status(hero, "Strength", 3)

def _impervious(hero, target, enemies):
    hero.gain_block(30)

def _barricade(hero, target, enemies):
    hero.barricade = True  # Block no longer resets

def _juggernaut(hero, target, enemies):
    hero.juggernaut = True  # Gaining block deals damage

def _corruption(hero, target, enemies):
    hero.corruption = True  # Skills cost 0 but exhaust

def _feed(hero, target, enemies):
    dmg = hero.calc_damage(10)
    if target:
        target.take_damage(dmg, attacker=hero)
        if target.current_hp <= 0:
            hero.max_hp += 3
            hero.current_hp = min(hero.current_hp + 3, hero.max_hp)

def _reaper(hero, target, enemies):
    total = 0
    for e in enemies:
        dmg = hero.calc_damage(4)
        e.take_damage(dmg, attacker=hero)
        total += dmg
    hero.heal(total)

def _fiend_fire(hero, target, enemies):
    n = len(hero.hand)
    for c in list(hero.hand):
        hero.hand.remove(c)
        hero.exhaust_pile.append(c)
    dmg = hero.calc_damage(7 * n)
    if target:
        target.take_damage(dmg, attacker=hero)

def _sentinel(hero, target, enemies):
    hero.gain_block(13 + hero.get_dexterity())
    # If exhausted, gain 2 energy — simplified: just block

def _seeing_red(hero, target, enemies):
    hero.energy += 2

def _wild_strike(hero, target, enemies):
    dmg = hero.calc_damage(12)
    if target:
        target.take_damage(dmg, attacker=hero)
    # Add a wound to draw pile
    hero.draw_pile.append(make_card("Wound"))

def _wound_effect(hero, target, enemies):
    pass  # Wound does nothing, just clogs hand

def _dark_embrace(hero, target, enemies):
    hero.dark_embrace = True  # Draw a card whenever you exhaust

def _evolve(hero, target, enemies):
    hero.evolve = True  # Draw a card when you receive a status card

def _feel_no_pain(hero, target, enemies):
    hero.feel_no_pain = True  # Gain block whenever you exhaust

def _metallicize(hero, target, enemies):
    hero.metallicize = (hero.metallicize or 0) + 3  # Gain 3 block at end of turn

def _combust(hero, target, enemies):
    hero.combust = (hero.combust or 0) + 1  # Lose 1 HP, deal 5 damage to all at end of turn

def _brutality(hero, target, enemies):
    hero.brutality = True  # Lose 1 HP, draw 1 card at start of turn

def _berserk(hero, target, enemies):
    _apply_status(hero, "Vulnerable", 2)
    hero.berserk = True  # Gain 1 energy at start of turn


# ─────────────────────────────────────────────
# Card Factory
# ─────────────────────────────────────────────

ALL_CARDS: dict[str, Card] = {}


def _register(card: Card):
    ALL_CARDS[card.name] = card
    return card


def _build_card_pool():
    cards = [
        # ── Starter ──
        Card("Strike",          1, ATTACK, STARTER,  "Deal 6 damage.",                                _strike),
        Card("Defend",          1, SKILL,  STARTER,  "Gain 5 Block.",                                 _defend, targeted=False),
        Card("Bash",            2, ATTACK, STARTER,  "Deal 8 damage. Apply 2 Vulnerable.",            _bash),

        # ── Common Attacks ──
        Card("Heavy Blade",     2, ATTACK, COMMON,   "Deal 14 damage.",                               _heavy_blade),
        Card("Twin Strike",     1, ATTACK, COMMON,   "Deal 5 damage twice.",                          _twin_strike),
        Card("Body Slam",       1, ATTACK, COMMON,   "Deal damage equal to your Block.",              _body_slam),
        Card("Pommel Strike",   1, ATTACK, COMMON,   "Deal 9 damage. Draw 1 card.",                   _pommel_strike),
        Card("Iron Wave",       1, ATTACK, COMMON,   "Deal 5 damage. Gain 5 Block.",                  _iron_wave),
        Card("Cleave",          1, ATTACK, COMMON,   "Deal 8 damage to ALL enemies.",                 _cleave, targeted=False),
        Card("Thunderclap",     1, ATTACK, COMMON,   "Deal 4 damage to ALL. Apply 1 Vulnerable.",     _thunderclap, targeted=False),
        Card("Headbutt",        1, ATTACK, COMMON,   "Deal 9 damage. Put top discard on draw pile.",  _headbutt),
        Card("Wild Strike",     1, ATTACK, COMMON,   "Deal 12 damage. Add a Wound to draw pile.",     _wild_strike),
        Card("Sword Boomerang", 1, ATTACK, COMMON,   "Deal 3 damage 3 times to random enemies.",      _sword_boomerang, targeted=False),
        Card("Perfected Strike",2, ATTACK, COMMON,   "Deal 6+2 damage per Strike in your deck.",      _perfected_strike),

        # ── Common Skills ──
        Card("Shrug It Off",    1, SKILL,  COMMON,   "Gain 8 Block. Draw 1 card.",                    _shrug_it_off, targeted=False),
        Card("True Grit",       1, SKILL,  COMMON,   "Gain 7 Block. Exhaust a random hand card.",     _true_grit, targeted=False),
        Card("Armaments",       1, SKILL,  COMMON,   "Gain 5 Block. Draw 1 card.",                    _armaments, targeted=False),
        Card("Seeing Red",      1, SKILL,  COMMON,   "Gain 2 Energy.",                                _seeing_red, targeted=False, exhausts=True),
        Card("Burning Pact",    1, SKILL,  COMMON,   "Exhaust a card. Draw 2 cards.",                 _burning_pact, targeted=False),
        Card("Bloodletting",    0, SKILL,  COMMON,   "Lose 3 HP. Gain 2 Energy.",                     _bloodletting, targeted=False),

        # ── Uncommon Attacks ──
        Card("Whirlwind",       -1, ATTACK, UNCOMMON, "Deal 5 damage to ALL enemies X times (X=Energy).", _whirlwind, targeted=False),
        Card("Fiend Fire",      2, ATTACK, UNCOMMON,  "Exhaust hand. Deal 7 damage per card.",         _fiend_fire, exhausts=True),
        Card("Feed",            1, ATTACK, UNCOMMON,  "Deal 10 damage. If fatal, gain 3 Max HP.",      _feed),
        Card("Reaper",          2, ATTACK, UNCOMMON,  "Deal 4 damage to ALL. Heal HP equal to damage.", _reaper, targeted=False),
        Card("Spot Weakness",   1, SKILL,  UNCOMMON,  "If enemy intends to attack, gain 3 Strength.",  _spot_weakness),

        # ── Uncommon Skills ──
        Card("Battle Trance",   0, SKILL,  UNCOMMON,  "Draw 3 cards.",                                 _battle_trance, targeted=False),
        Card("Second Wind",     1, SKILL,  UNCOMMON,  "Exhaust non-Attack cards. Gain 5 Block each.",  _second_wind, targeted=False),
        Card("Entrench",        2, SKILL,  UNCOMMON,  "Double your Block.",                             _entrench, targeted=False),
        Card("Flame Barrier",   2, SKILL,  UNCOMMON,  "Gain 12 Block. Gain 4 Thorns.",                 _flame_barrier, targeted=False),
        Card("Offering",        0, SKILL,  UNCOMMON,  "Lose 6 HP. Gain 2 Energy. Draw 3 cards.",       _offering, targeted=False, exhausts=True),
        Card("Sentinel",        1, SKILL,  UNCOMMON,  "Gain 13 Block.",                                 _sentinel, targeted=False),

        # ── Uncommon Powers ──
        Card("Inflame",         1, POWER,  UNCOMMON,  "Gain 2 Strength.",                              _inflame, targeted=False),
        Card("Flex",            0, POWER,  UNCOMMON,  "Gain 2 Strength.",                              _flex, targeted=False),
        Card("Dark Embrace",    2, POWER,  UNCOMMON,  "Whenever you Exhaust, draw 1 card.",            _dark_embrace, targeted=False),
        Card("Feel No Pain",    1, POWER,  UNCOMMON,  "Whenever you Exhaust, gain 3 Block.",           _feel_no_pain, targeted=False),
        Card("Metallicize",     1, POWER,  UNCOMMON,  "At end of turn, gain 3 Block.",                 _metallicize, targeted=False),
        Card("Brutality",       0, POWER,  UNCOMMON,  "At start of turn, lose 1 HP and draw 1 card.", _brutality, targeted=False),
        Card("Berserk",         0, POWER,  UNCOMMON,  "Gain 2 Vulnerable. At start of turn, gain 1 Energy.", _berserk, targeted=False),

        # ── Rare Attacks ──
        Card("Limit Break",     1, SKILL,  RARE,      "Double your Strength.",                         _limit_break, targeted=False, exhausts=True),
        Card("Impervious",      2, SKILL,  RARE,      "Gain 30 Block.",                                _impervious, targeted=False, exhausts=True),

        # ── Rare Powers ──
        Card("Barricade",       3, POWER,  RARE,      "Block no longer resets at start of turn.",      _barricade, targeted=False),
        Card("Juggernaut",      2, POWER,  RARE,      "Whenever you gain Block, deal 5 damage to a random enemy.", _juggernaut, targeted=False),
        Card("Corruption",      3, POWER,  RARE,      "Skills cost 0. Whenever you play a Skill, Exhaust it.", _corruption, targeted=False),
        Card("Combust",         1, POWER,  RARE,      "At end of turn, lose 1 HP and deal 5 damage to ALL.", _combust, targeted=False),
        Card("Evolve",          1, POWER,  RARE,      "Whenever you receive a status card, draw 1 card.", _evolve, targeted=False),

        # ── Unplayable ──
        Card("Wound",           -1, SKILL, STARTER,  "Unplayable. Clogs your hand.",                  _wound_effect, targeted=False),
    ]
    for c in cards:
        _register(c)


_build_card_pool()


def make_card(name: str) -> Card:
    """Return a fresh copy of a named card."""
    if name not in ALL_CARDS:
        raise ValueError(f"Unknown card: {name}")
    return ALL_CARDS[name].copy()


def get_starter_deck() -> list[Card]:
    deck = []
    for _ in range(5):
        deck.append(make_card("Strike"))
    for _ in range(4):
        deck.append(make_card("Defend"))
    deck.append(make_card("Bash"))
    return deck


def get_reward_cards(rarity_weights=None, n=3) -> list[Card]:
    """Return N random cards suitable as combat rewards."""
    if rarity_weights is None:
        rarity_weights = {COMMON: 60, UNCOMMON: 30, RARE: 10}

    pool = [c for c in ALL_CARDS.values()
            if c.rarity in rarity_weights and c.name not in ("Wound",)]

    # Weighted sample
    weighted = []
    for c in pool:
        weighted.extend([c] * rarity_weights.get(c.rarity, 0))

    chosen = []
    seen = set()
    random.shuffle(weighted)
    for c in weighted:
        if c.name not in seen:
            chosen.append(c.copy())
            seen.add(c.name)
        if len(chosen) == n:
            break
    return chosen


def get_merchant_cards(n=5) -> list[tuple[Card, int]]:
    """Return N cards with prices for the merchant."""
    import random as _r
    from src.constants import CARD_PRICE_MIN, CARD_PRICE_MAX
    pool = [c for c in ALL_CARDS.values()
            if c.rarity not in (STARTER,) and c.name not in ("Wound",)]
    chosen = _r.sample(pool, min(n, len(pool)))
    result = []
    for c in chosen:
        price = _r.randint(CARD_PRICE_MIN, CARD_PRICE_MAX)
        result.append((c.copy(), price))
    return result
