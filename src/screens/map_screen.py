"""
Map Screen — shows the dungeon node list and lets the player enter the next node.
"""
import pygame
import math
from src.constants import *
from src.screens.ui_utils import draw_text, draw_button, draw_panel, draw_bar, get_font
from src.systems.dungeon import *
from src.localization import t


class MapScreen:
    def __init__(self):
        self.font_title = get_font(36, bold=True)
        self.font       = get_font(22)
        self.font_small = get_font(16)
        self.font_btn   = get_font(24, bold=True)

        # ── Asset Loading ──
        self.icons = {}
        icon_files = {
            NODE_ENEMY:    "enemy_icon.png", # Fallback if specific Slime isn't used
            NODE_ELITE:    "node_elite.png",
            NODE_BOSS:     "node_boss.png",
            NODE_CHEST:    "node_chest.png",
            NODE_MERCHANT: "node_merchant.png",
            NODE_EVENT:    "node_event.png",
        }
        for ntype, fname in icon_files.items():
            try:
                path = f"assets/icons/{fname}"
                img = pygame.image.load(path).convert_alpha()
                self.icons[ntype] = pygame.transform.scale(img, (32, 32))
            except:
                self.icons[ntype] = None

        # Specific assets
        try:
            self.relic_images = {
                "Fire Pendant": pygame.transform.scale(pygame.image.load("assets/icons/Fire_pendant.png").convert_alpha(), (24, 24)),
                "Kryptonite":   pygame.transform.scale(pygame.image.load("assets/icons/kriptonite.png").convert_alpha(), (24, 24)),
            }
        except:
            self.relic_images = {}

        # ── Background Loading ──
        try:
            self.bg_img = pygame.image.load("assets/Dungeon_background.png").convert()
            self.bg_img = pygame.transform.scale(self.bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            self.bg_img = None

        # ── Scrolling state ──
        self.scroll_y = 0.0
        self.target_scroll_y = 0.0
        self.scroll_speed = 10.0

    def handle_event(self, event, game_state) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            dungeon = game_state.dungeon
            
            # 1. Check node clicks
            nodes_by_floor = dungeon.get_nodes_by_floor()
            scroll_offset = int(self.scroll_y)
            
            for floor, nodes in nodes_by_floor.items():
                for node in nodes:
                    rect = self._get_node_rect(node, scroll_offset)
                    if rect.collidepoint(mx, my):
                        if node.reachable:
                            game_state.select_node(node.id)
                            return True

            # 2. Check Enter button
            btn_w, btn_h = 300, 60
            enter_rect = pygame.Rect(SCREEN_WIDTH // 2 - btn_w // 2, SCREEN_HEIGHT - 95, btn_w, btn_h)
            if enter_rect.collidepoint(mx, my):
                game_state.enter_node()
                return True
        elif event.type == pygame.MOUSEWHEEL:
            # Multiply by sensitivity factor
            self.target_scroll_y -= event.y * 50
            return True
            
        return False

    def _get_scroll_offset(self, dungeon) -> int:
        return int(self.scroll_y)

    def _get_node_rect(self, node, scroll_offset: int) -> pygame.Rect:
        floor_h = 100
        node_spacing = 150
        
        # Bottom-up rendering: Floor 1 is near bottom
        y = SCREEN_HEIGHT - 200 - (node.floor * floor_h) + scroll_offset
        x = SCREEN_WIDTH // 2 - (2.5 * node_spacing) + (node.x_pos * node_spacing) + 125
        return pygame.Rect(x - 24, y - 24, 48, 48)

    def update(self, dt):
        # ── Smooth scrolling ──
        # Simple lerp / exponential decay
        self.scroll_y += (self.target_scroll_y - self.scroll_y) * 0.1
        
        # ── Clamping ──
        # Act length is 15. Floor height is 100.
        # Max scroll should be around (15 * 100) - window_height
        max_scroll = 15 * 100 - 400 
        self.target_scroll_y = max(0, min(self.target_scroll_y, max_scroll))
        self.scroll_y = max(0, min(self.scroll_y, max_scroll))

    def draw(self, surface, game_state):
        if self.bg_img:
            surface.blit(self.bg_img, (0, 0))
            # Dim the background for legibility
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160)) # Semi-transparent black
            surface.blit(overlay, (0, 0))
        else:
            surface.fill(DARK_BG)

        hero = game_state.hero
        dungeon = game_state.dungeon

        # ── Title ──
        draw_text(surface, t("map.title"), SCREEN_WIDTH // 2, 30,
                  self.font_title, GOLD, center=True)

        # ── Hero stats panel ──
        # Larger panel with more padding
        panel_y = 70
        panel_h = 180
        draw_panel(surface, 20, panel_y, 280, panel_h, color=(30, 25, 50, 200), border_color=(100, 90, 150))
        
        draw_text(surface, hero.name, 35, panel_y + 15, self.font, WHITE)
        draw_text(surface, f"{t('map.floor')} {dungeon.current_floor}", 35, panel_y + 45, self.font_small, LIGHT_GREY)
        
        # HP Bar
        draw_bar(surface, 35, panel_y + 75, 230, 22, hero.current_hp, hero.max_hp,
                 HP_BAR_FG, HP_BAR_BG, f"{t('hero.hp')} {hero.current_hp}/{hero.max_hp}")
        
        draw_text(surface, f"{t('map.gold')} {hero.gold}", 35, panel_y + 110, self.font_small, GOLD)

        # ── Relics ──
        # Expanded relic boxes with better spacing
        relic_y = panel_y + 135
        relic_x = 35
        for r in hero.relics:
            # Draw relic box (wider)
            rw, rh = 120, 28
            pygame.draw.rect(surface, PURPLE, (relic_x, relic_y, rw, rh), border_radius=6)
            pygame.draw.rect(surface, (200, 150, 255), (relic_x, relic_y, rw, rh), 1, border_radius=6)
            
            # Draw relic icon if available
            img = self.relic_images.get(r.name)
            tx_offset = 6
            if img:
                surface.blit(img, (relic_x + 4, relic_y + 2))
                tx_offset = 32

            # Simple text clipping/elipsis if too long
            name_text = t("relic.name." + r.name)
            available_w = rw - tx_offset - 4
            if self.font_small.size(name_text)[0] > available_w:
                name_text = name_text[:10] + ".."
                
            draw_text(surface, name_text, relic_x + tx_offset, relic_y + 4, self.font_small, WHITE, shadow=True)
            relic_x += rw + 10
            if relic_x > 260: # Wrap if too many relics for the panel width
                relic_x = 35
                relic_y += rh + 5

        # ── Branching Map Graph ──
        scroll_offset = self._get_scroll_offset(dungeon)
        nodes_by_floor = dungeon.get_nodes_by_floor()
        
        # Draw connections first (behind nodes)
        for node in dungeon.nodes.values():
            start_rect = self._get_node_rect(node, scroll_offset)
            for child_id in node.children_ids:
                child = dungeon.nodes.get(child_id)
                if child:
                    end_rect = self._get_node_rect(child, scroll_offset)
                    # Color based on reachability/completion
                    line_col = GREY
                    if node.completed and child.reachable:
                        line_col = GOLD
                    elif node.completed and child.completed:
                        line_col = WHITE
                    
                    pygame.draw.line(surface, line_col, start_rect.center, end_rect.center, 3)

        # Draw nodes
        mx, my = pygame.mouse.get_pos()
        for floor, nodes in nodes_by_floor.items():
            for node in nodes:
                rect = self._get_node_rect(node, scroll_offset)
                color = NODE_COLORS.get(node.node_type, GREY)
                icon_img = self.icons.get(node.node_type)
                
                # Highlight current/selected
                if node.current:
                    pygame.draw.circle(surface, GOLD, rect.center, 32, 3)
                    pygame.draw.circle(surface, (*GOLD, 40), rect.center, 30)
                elif node.reachable:
                    # Pulsing highlight for reachable
                    pulse = int(5 * math.sin(pygame.time.get_ticks() * 0.005))
                    pygame.draw.circle(surface, (200, 200, 200), rect.center, 28 + pulse, 2)
                
                # Draw node base
                base_col = (30, 30, 40)
                if node.completed:
                    base_col = (50, 50, 60)
                pygame.draw.circle(surface, base_col, rect.center, 24)
                pygame.draw.circle(surface, color if not node.completed else GREY, rect.center, 24, 2)

                # Draw icon
                if icon_img:
                    icon_rect = icon_img.get_rect(center=rect.center)
                    if node.completed:
                        # Draw grayscale or dark if completed? For now just draw normal.
                        surface.blit(icon_img, icon_rect)
                    else:
                        surface.blit(icon_img, icon_rect)
                else:
                    icon = NODE_ICONS.get(node.node_type, "?")
                    draw_text(surface, icon, rect.centerx, rect.centery - 10, self.font, WHITE, center=True)

                # Label (Floor)
                # draw_text(surface, str(node.floor), rect.centerx, rect.centery + 15, self.font_small, LIGHT_GREY, center=True)

        # ── Enter button ──
        mx, my = pygame.mouse.get_pos()
        node = dungeon.current_node()
        if node:
            btn_w, btn_h = 300, 60
            enter_rect = pygame.Rect(SCREEN_WIDTH // 2 - btn_w // 2, SCREEN_HEIGHT - 95, btn_w, btn_h)
            node_color = NODE_COLORS.get(node.node_type, PANEL_BG)
            enter_label = f"{t('map.enter')}  {NODE_ICONS.get(node.node_type, '')}  {t('node.' + node.node_type)}"
            draw_button(surface, enter_rect,
                        enter_label,
                        self.font_btn,
                        color=(*node_color[:3],),
                        hover_color=tuple(min(255, c + 40) for c in node_color[:3]),
                        border_color=node_color,
                        mouse_pos=(mx, my))

        # ── Deck count ──
        draw_text(surface, f"{t('map.deck')} {len(hero.deck)} {t('map.cards')}",
                  SCREEN_WIDTH - 200, SCREEN_HEIGHT - 40, self.font_small, LIGHT_GREY)
