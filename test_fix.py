
import pygame
from src.constants import *
from src.game_state import GameState
from src.screens.map_screen import MapScreen
from src.screens.combat_screen import CombatScreen

def test_transition():
    pygame.init()
    pygame.display.set_mode((1, 1)) # Minimized window for testing
    
    gs = GameState()
    gs.new_game() # Should go to STATE_MAP
    
    screens = {
        STATE_MAP: MapScreen(),
        STATE_COMBAT: CombatScreen()
    }
    
    dt = 0.016
    
    # ── Simulate clicking Enter on an enemy node ──
    # MapScreen.handle_event(gs.enter_node) will change gs.state to STATE_COMBAT
    
    current_screen = screens.get(gs.state)
    print(f"Current state: {gs.state}, Screen: {type(current_screen).__name__}")
    
    # Trigger the state change manually (simulating enter_node)
    gs.enter_node()
    print(f"New state: {gs.state}")
    
    # The fix in main.py is:
    current_screen = screens.get(gs.state) # This is what I added
    
    print(f"Updating screen: {type(current_screen).__name__}")
    if current_screen:
        if gs.state == STATE_COMBAT:
            current_screen.update(dt, gs)
        elif hasattr(current_screen, 'update'):
            try:
                current_screen.update(dt)
            except TypeError:
                current_screen.update(dt, gs)
    
    print("Success: No TypeError during transition update.")
    pygame.quit()

if __name__ == "__main__":
    test_transition()
