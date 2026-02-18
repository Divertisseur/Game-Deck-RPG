"""
GameDeckRPG - Constants and Configuration
"""

# Screen
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TITLE = "GameDeckRPG"

# Colors
BLACK       = (0, 0, 0)
WHITE       = (255, 255, 255)
DARK_BG     = (15, 12, 25)
PANEL_BG    = (25, 20, 40)
CARD_BG     = (35, 30, 55)
CARD_HOVER  = (55, 48, 85)
CARD_BORDER = (80, 70, 120)

RED         = (220, 60, 60)
DARK_RED    = (140, 30, 30)
GREEN       = (60, 200, 100)
DARK_GREEN  = (30, 120, 60)
BLUE        = (60, 120, 220)
DARK_BLUE   = (30, 60, 140)
GOLD        = (255, 200, 50)
ORANGE      = (255, 140, 30)
PURPLE      = (160, 80, 220)
CYAN        = (60, 200, 220)
PINK        = (220, 80, 160)
GREY        = (120, 120, 140)
LIGHT_GREY  = (180, 180, 200)

HP_BAR_BG   = (80, 20, 20)
HP_BAR_FG   = (200, 50, 50)
BLOCK_COLOR = (80, 140, 200)
ENERGY_COLOR= (220, 180, 50)

ATTACK_COLOR = (220, 80, 80)
SKILL_COLOR  = (80, 140, 220)
POWER_COLOR  = (160, 80, 220)

# Card dimensions
CARD_W = 120
CARD_H = 170
CARD_HAND_Y = SCREEN_HEIGHT - CARD_H - 20

# Game settings
STARTING_HP = 80
STARTING_ENERGY = 3
HAND_SIZE = 5
STARTING_GOLD = 0

# Floor settings
BOSS_EVERY = 5       # Boss appears every N floors
ELITE_FLOOR_MIN = 3  # Elites don't appear before this floor

# Merchant prices
CARD_PRICE_MIN = 50
CARD_PRICE_MAX = 150
RELIC_PRICE = 200
REMOVE_PRICE = 75

# Difficulty scaling per floor
def enemy_hp_scale(floor: int) -> float:
    return 1.0 + (floor - 1) * 0.15

def enemy_dmg_scale(floor: int) -> float:
    return 1.0 + (floor - 1) * 0.12

# Node type weights (floor-dependent)
def get_node_weights(floor: int) -> dict:
    if floor % BOSS_EVERY == 0:
        return {"boss": 1}
    weights = {
        "enemy":    50,
        "elite":    0 if floor < ELITE_FLOOR_MIN else 15,
        "chest":    15,
        "merchant": 10,
        "event":    10,
    }
    return weights

# Screen states
STATE_MAIN_MENU   = "main_menu"
STATE_MAP         = "map"
STATE_COMBAT      = "combat"
STATE_CARD_REWARD = "card_reward"
STATE_MERCHANT    = "merchant"
STATE_CHEST       = "chest"
STATE_EVENT       = "event"
STATE_SETTINGS    = "settings"
STATE_GAME_OVER   = "game_over"
STATE_VICTORY     = "victory"
