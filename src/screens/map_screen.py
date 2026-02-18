"""
Map Screen — shows the dungeon node list and lets the player enter the next node.
"""
import pygame
from src.constants import *
from src.screens.ui_utils import draw_text, draw_button, draw_panel, draw_bar, get_font
from src.systems.dungeon import NODE_ICONS, NODE_COLORS
from src.localization import t


class MapScreen:
    def __init__(self):
        self.font_title = get_font(36, bold=True)
        self.font       = get_font(22)
        self.font_small = get_font(16)
        self.font_btn   = get_font(24, bold=True)

    def handle_event(self, event, game_state) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            btn_w, btn_h = 300, 60
            enter_rect = pygame.Rect(SCREEN_WIDTH // 2 - btn_w // 2, SCREEN_HEIGHT - 95, btn_w, btn_h)
            if enter_rect.collidepoint(mx, my):
                game_state.enter_node()
                return True
        return False

    def update(self, dt):
        pass

    def draw(self, surface, game_state):
        surface.fill(DARK_BG)
        hero = game_state.hero
        dungeon = game_state.dungeon

        # ── Title ──
        draw_text(surface, t("map.title"), SCREEN_WIDTH // 2, 30,
                  self.font_title, GOLD, center=True)

        # ── Hero stats panel ──
        draw_panel(surface, 20, 70, 260, 130)
        draw_text(surface, hero.name, 30, 80, self.font, WHITE)
        draw_text(surface, f"{t('map.floor')} {dungeon.current_floor}", 30, 108, self.font_small, LIGHT_GREY)
        draw_bar(surface, 30, 130, 200, 18, hero.current_hp, hero.max_hp,
                 HP_BAR_FG, HP_BAR_BG, f"{t('hero.hp')} {hero.current_hp}/{hero.max_hp}")
        draw_text(surface, f"{t('map.gold')} {hero.gold}", 30, 158, self.font_small, GOLD)

        # ── Relics ──
        relic_x = 30
        for r in hero.relics:
            pygame.draw.rect(surface, PURPLE, (relic_x, 185, 80, 22), border_radius=4)
            draw_text(surface, r.name[:10], relic_x + 2, 187, self.font_small, WHITE, shadow=False)
            relic_x += 90

        # ── Node list ──
        # Show last 10 nodes
        nodes = dungeon.nodes[-10:] if len(dungeon.nodes) > 10 else dungeon.nodes
        list_w = 460
        list_x = SCREEN_WIDTH // 2 - list_w // 2
        list_y = 80
        for node in nodes:
            color = NODE_COLORS.get(node.node_type, GREY)
            icon  = NODE_ICONS.get(node.node_type, "?")
            
            if node.current:
                # Highlight current node
                pygame.draw.rect(surface, (*color, 40),
                                 (list_x - 10, list_y - 5, list_w + 20, 44),
                                 border_radius=8)
                pygame.draw.rect(surface, color,
                                 (list_x - 10, list_y - 5, list_w + 20, 44),
                                 2, border_radius=8)

            status = t("map.current") if node.current else (t("map.done") if node.completed else "")
            node_name = t(f"node.{node.node_type}")
            label = f"{t('map.floor')} {node.floor}  {icon}  {node_name}"
            col = color if node.current else (GREY if node.completed else LIGHT_GREY)
            
            # Draw label
            draw_text(surface, label, list_x + 10, list_y + 5, self.font, col)
            
            # Draw status (right-aligned)
            if status:
                status_font = self.font_small
                tw = status_font.size(status)[0]
                draw_text(surface, status, list_x + list_w - tw - 10, list_y + 9, status_font,
                          GOLD if node.current else GREEN)
            list_y += 50

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
