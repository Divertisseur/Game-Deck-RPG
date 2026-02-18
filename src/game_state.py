"""
Game State Manager — central hub for all screen transitions.
"""
from __future__ import annotations
from src.constants import *
from src.models.hero import Hero
from src.models.card import get_starter_deck
from src.models.relic import get_starter_relic
from src.systems.dungeon import Dungeon, NODE_ENEMY, NODE_ELITE, NODE_BOSS, NODE_CHEST, NODE_MERCHANT, NODE_EVENT


class GameState:
    def __init__(self):
        self.state = STATE_MAIN_MENU
        self.hero: Hero = None
        self.dungeon: Dungeon = None
        self.combat_state = None
        self.card_reward_pool = []
        self.merchant_cards = []
        self.chest_reward = None
        self.current_event = None
        self.previous_state = None

    def new_game(self):
        """Initialize a fresh run."""
        self.hero = Hero()
        self.hero.deck = get_starter_deck()
        self.hero.add_relic(get_starter_relic())
        self.dungeon = Dungeon()
        self.combat_state = None
        self.card_reward_pool = []
        self.go_to(STATE_MAP)

    def go_to(self, state: str):
        self.previous_state = self.state
        self.state = state

    def enter_node(self):
        """Called when player clicks 'Enter' on the current node."""
        node = self.dungeon.current_node()
        if node is None:
            return

        if node.node_type in (NODE_ENEMY, NODE_ELITE, NODE_BOSS):
            self._start_combat(node)
        elif node.node_type == NODE_CHEST:
            self._open_chest()
        elif node.node_type == NODE_MERCHANT:
            self._open_merchant()
        elif node.node_type == NODE_EVENT:
            self._trigger_event()

    def _start_combat(self, node):
        from src.models.enemy import get_enemy_for_floor, get_elite_for_floor
        from src.systems.combat import CombatState
        floor = node.floor
        if node.node_type == NODE_ELITE:
            enemies = [get_elite_for_floor(floor)]
        else:
            enemies = [get_enemy_for_floor(floor)]
        self.combat_state = CombatState(self.hero, enemies)
        self.combat_state.start_combat()
        self.go_to(STATE_COMBAT)

    def _open_chest(self):
        from src.models.relic import get_chest_reward
        import random
        # Chest gives gold + sometimes a relic
        gold = random.randint(25, 60)
        self.hero.gold += gold
        relic = get_chest_reward()
        self.chest_reward = {"gold": gold, "relic": relic}
        self.go_to(STATE_CHEST)

    def _open_merchant(self):
        from src.models.card import get_merchant_cards
        self.merchant_cards = get_merchant_cards(5)
        self.go_to(STATE_MERCHANT)

    def _trigger_event(self):
        from src.systems.dungeon import get_random_event
        self.current_event = get_random_event()
        self.go_to(STATE_EVENT)

    def combat_won(self):
        """Called after combat victory."""
        from src.models.card import get_reward_cards
        self.card_reward_pool = get_reward_cards(n=3)
        self.dungeon.complete_current_node()
        self.go_to(STATE_CARD_REWARD)

    def skip_card_reward(self):
        self.card_reward_pool = []
        self.go_to(STATE_MAP)

    def pick_card_reward(self, card):
        self.hero.add_card_to_deck(card)
        self.card_reward_pool = []
        self.go_to(STATE_MAP)

    def complete_chest(self, take_relic: bool):
        if take_relic and self.chest_reward:
            self.hero.add_relic(self.chest_reward["relic"])
        self.chest_reward = None
        self.dungeon.complete_current_node()
        self.go_to(STATE_MAP)

    def complete_merchant(self):
        self.merchant_cards = []
        self.dungeon.complete_current_node()
        self.go_to(STATE_MAP)

    def complete_event(self):
        self.current_event = None
        self.dungeon.complete_current_node()
        self.go_to(STATE_MAP)

    def game_over(self):
        self.go_to(STATE_GAME_OVER)
