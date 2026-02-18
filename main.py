"""
GameDeckRPG — Main Entry Point
"""
import sys
import pygame
from src.constants import *
from src.game_state import GameState
from src.screens.main_menu import MainMenuScreen
from src.screens.map_screen import MapScreen
from src.screens.combat_screen import CombatScreen
from src.screens.card_reward_screen import CardRewardScreen
from src.screens.merchant_screen import MerchantScreen
from src.screens.chest_screen import ChestScreen
from src.screens.event_screen import EventScreen
from src.screens.settings_screen import SettingsScreen
from src.screens.game_over_screen import GameOverScreen


def main():
    pygame.init()
    pygame.display.set_caption(TITLE)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # Game state
    gs = GameState()

    # Screens
    screens = {
        STATE_MAIN_MENU:   MainMenuScreen(),
        STATE_MAP:         MapScreen(),
        STATE_COMBAT:      CombatScreen(),
        STATE_CARD_REWARD: CardRewardScreen(),
        STATE_MERCHANT:    MerchantScreen(),
        STATE_CHEST:       ChestScreen(),
        STATE_EVENT:       EventScreen(),
        STATE_SETTINGS:    SettingsScreen(),
        STATE_GAME_OVER:   GameOverScreen(),
    }

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        current_screen = screens.get(gs.state)

        # ── Events ──
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if gs.state == STATE_MAIN_MENU:
                    running = False
                else:
                    gs.go_to(STATE_MAIN_MENU)
            if current_screen:
                current_screen.handle_event(event, gs)

        # ── Update ──
        current_screen = screens.get(gs.state)
        if current_screen:
            if gs.state == STATE_COMBAT:
                current_screen.update(dt, gs)
            elif hasattr(current_screen, 'update'):
                try:
                    current_screen.update(dt)
                except TypeError:
                    current_screen.update(dt, gs)

        # ── Draw ──
        current_screen = screens.get(gs.state)
        if current_screen:
            if gs.state in (STATE_MAP, STATE_COMBAT, STATE_CARD_REWARD,
                            STATE_MERCHANT, STATE_CHEST, STATE_EVENT, STATE_GAME_OVER):
                try:
                    current_screen.draw(screen, gs)
                except TypeError:
                    current_screen.draw(screen)
            else:
                current_screen.draw(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
