"""
Dungeon system — floor/node generation and progression.
"""
from __future__ import annotations
import random
from dataclasses import dataclass, field
from typing import Optional


NODE_ENEMY    = "enemy"
NODE_ELITE    = "elite"
NODE_BOSS     = "boss"
NODE_CHEST    = "chest"
NODE_MERCHANT = "merchant"
NODE_EVENT    = "event"

NODE_ICONS = {
    NODE_ENEMY:    "⚔",
    NODE_ELITE:    "💀",
    NODE_BOSS:     "👑",
    NODE_CHEST:    "📦",
    NODE_MERCHANT: "🛒",
    NODE_EVENT:    "❓",
}

NODE_COLORS = {
    NODE_ENEMY:    (200, 60, 60),
    NODE_ELITE:    (160, 40, 200),
    NODE_BOSS:     (220, 160, 20),
    NODE_CHEST:    (60, 180, 80),
    NODE_MERCHANT: (60, 140, 220),
    NODE_EVENT:    (180, 180, 60),
}


@dataclass
class DungeonNode:
    id: str
    floor: int
    node_type: str
    x_pos: int                      # Horizontal position index (0 to width-1)
    children_ids: list[str] = field(default_factory=list)
    completed: bool = False
    current: bool = False
    reachable: bool = False          # Can the player move here?


class Dungeon:
    def __init__(self):
        self.current_floor = 0
        self.nodes: dict[str, DungeonNode] = {} # id -> node
        self.width = 5 # Number of parallel paths
        self.act_length = 15
        self._generate_act()

    def _generate_act(self):
        """Generate a structured branching graph for the entire act."""
        from src.constants import get_node_weights, BOSS_EVERY
        
        # 1. Create nodes by floor
        floors: list[list[DungeonNode]] = []
        for f in range(1, self.act_length):
            floor_nodes = []
            num_nodes = random.randint(3, self.width)
            
            # Distribute nodes horizontally
            x_positions = sorted(random.sample(range(self.width), num_nodes))
            
            for x in x_positions:
                node_id = f"f{f}_x{x}"
                weights = get_node_weights(f)
                
                # Floor 1 is usually combat
                if f == 1:
                    node_type = NODE_ENEMY
                else:
                    node_type = random.choices(list(weights.keys()), weights=list(weights.values()))[0]
                
                node = DungeonNode(id=node_id, floor=f, node_type=node_type, x_pos=x)
                floor_nodes.append(node)
                self.nodes[node_id] = node
            floors.append(floor_nodes)

        # 2. Add Boss Node
        boss_id = f"f{self.act_length}_x{self.width // 2}"
        boss_node = DungeonNode(id=boss_id, floor=self.act_length, node_type=NODE_BOSS, x_pos=self.width // 2)
        self.nodes[boss_id] = boss_node
        floors.append([boss_node])

        # 3. Create connections
        for f in range(len(floors) - 1):
            current_floor_nodes = floors[f]
            next_floor_nodes = floors[f + 1]
            
            for node in current_floor_nodes:
                # Find nodes in next floor that are "reachable" (x separation <= 1)
                potentials = [n for n in next_floor_nodes if abs(n.x_pos - node.x_pos) <= 1]
                
                # If no direct neighbors, bridge to the closest
                if not potentials:
                    potentials = [min(next_floor_nodes, key=lambda n: abs(n.x_pos - node.x_pos))]
                
                for p in potentials:
                    node.children_ids.append(p.id)

            # Ensure every node in 'next_floor' has at least one parent (prevents dead ends)
            for target in next_floor_nodes:
                if not any(target.id in n.children_ids for n in current_floor_nodes):
                    parent = min(current_floor_nodes, key=lambda n: abs(n.x_pos - target.x_pos))
                    parent.children_ids.append(target.id)

        # Initial state: First floor nodes are current options? 
        # Actually, in STS you pick one to start. We'll mark Floor 1 as reachable.
        for node in floors[0]:
            node.reachable = True

    def current_node(self) -> Optional[DungeonNode]:
        for n in self.nodes.values():
            if n.current:
                return n
        return None

    def select_node(self, node_id: str):
        """Player picks a reachable node."""
        node = self.nodes.get(node_id)
        if node and node.reachable:
            # Deselect current
            curr = self.current_node()
            if curr:
                curr.current = False
            
            node.current = True
            return True
        return False

    def complete_current_node(self):
        node = self.current_node()
        if node:
            node.completed = True
            node.current = False
            self.current_floor = node.floor
            
            # Clear previous reachable
            for n in self.nodes.values():
                n.reachable = False
                
            # Set next reachable
            for cid in node.children_ids:
                if cid in self.nodes:
                    self.nodes[cid].reachable = True

    def get_nodes_by_floor(self) -> dict[int, list[DungeonNode]]:
        by_floor = {}
        for n in self.nodes.values():
            if n.floor not in by_floor:
                by_floor[n.floor] = []
            by_floor[n.floor].append(n)
        return by_floor


# ─────────────────────────────────────────────
# Random Events
# ─────────────────────────────────────────────

@dataclass
class EventChoice:
    text: str
    effect_fn: object  # callable(hero) -> str message


@dataclass
class Event:
    title: str
    description: str
    choices: list[EventChoice]


def _heal_25(hero):
    amt = int(hero.max_hp * 0.25)
    hero.heal(amt)
    return f"You feel refreshed. Healed {amt} HP."

def _lose_hp_gain_gold(hero):
    amt = int(hero.max_hp * 0.10)
    hero.take_damage(amt, ignore_block=True)
    hero.gold += 50
    return f"You paid {amt} HP for 50 gold."

def _gain_max_hp(hero):
    hero.max_hp += 5
    hero.current_hp = min(hero.current_hp + 5, hero.max_hp)
    return "Your max HP increased by 5!"

def _gain_gold(hero):
    hero.gold += 75
    return "You found 75 gold!"

def _lose_gold(hero):
    lost = min(hero.gold, 50)
    hero.gold -= lost
    return f"You lost {lost} gold."

def _gain_strength(hero):
    from src.models.status import make_status
    hero.apply_status(make_status("Strength", 1))
    return "You feel stronger! +1 Strength (permanent)."

def _gain_card(hero):
    from src.models.card import get_reward_cards
    cards = get_reward_cards(n=1)
    if cards:
        hero.add_card_to_deck(cards[0])
        return f"Added {cards[0].name} to your deck."
    return "Nothing happened."

def _remove_card(hero):
    if len(hero.deck) > 1:
        import random
        card = random.choice(hero.deck)
        hero.remove_card_from_deck(card)
        return f"Removed {card.name} from your deck."
    return "Your deck is too small to remove a card."

def _nothing(hero):
    return "Nothing happens. You move on."


EVENTS = [
    Event(
        "Ancient Shrine",
        "You find an ancient shrine. Strange runes glow faintly.",
        [
            EventChoice("Pray (Heal 25% HP)", _heal_25),
            EventChoice("Offer blood (Lose 10% HP, gain 50 gold)", _lose_hp_gain_gold),
            EventChoice("Leave", _nothing),
        ]
    ),
    Event(
        "Mysterious Merchant",
        "A hooded figure offers you a deal.",
        [
            EventChoice("Buy strength (+1 Strength, -50 gold)", lambda h: _gain_strength(h) if h.gold >= 50 and not h.__setattr__('gold', h.gold - 50) else "Not enough gold."),
            EventChoice("Ignore and leave", _nothing),
        ]
    ),
    Event(
        "Forgotten Library",
        "Dusty tomes line the walls. One book glows.",
        [
            EventChoice("Read the book (Add a random card)", _gain_card),
            EventChoice("Burn a book (Remove a random card)", _remove_card),
            EventChoice("Leave", _nothing),
        ]
    ),
    Event(
        "Treasure Room",
        "A small chest sits in the center of the room.",
        [
            EventChoice("Open it (Gain 75 gold)", _gain_gold),
            EventChoice("Leave it (Suspicious...)", _nothing),
        ]
    ),
    Event(
        "Cursed Tome",
        "A dark tome whispers your name.",
        [
            EventChoice("Read it (Gain 5 Max HP, lose 10 gold)", lambda h: _gain_max_hp(h) if not h.__setattr__('gold', max(0, h.gold - 10)) else ""),
            EventChoice("Burn it (Gain 30 gold)", lambda h: setattr(h, 'gold', h.gold + 30) or "You burn the tome. Gained 30 gold."),
            EventChoice("Ignore", _nothing),
        ]
    ),
    Event(
        "Bandit Ambush",
        "Bandits jump out! They demand your gold.",
        [
            EventChoice("Pay them (Lose 50 gold)", _lose_gold),
            EventChoice("Fight back (Lose 15 HP)", lambda h: h.take_damage(15, ignore_block=True) or "You fight them off, but take 15 damage."),
        ]
    ),
    Event(
        "Healing Fountain",
        "A crystal-clear fountain bubbles with magical water.",
        [
            EventChoice("Drink (Heal 25% HP)", _heal_25),
            EventChoice("Fill your flask (Gain 5 Max HP)", _gain_max_hp),
        ]
    ),
    Event(
        "Wandering Merchant",
        "A merchant lost in the dungeon offers a quick deal.",
        [
            EventChoice("Buy a random card (75 gold)", lambda h: _gain_card(h) if h.gold >= 75 and not h.__setattr__('gold', h.gold - 75) else "Not enough gold."),
            EventChoice("Leave", _nothing),
        ]
    ),
]


def get_random_event() -> Event:
    return random.choice(EVENTS)
