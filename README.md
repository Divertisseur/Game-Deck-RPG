# GameDeckRPG

A roguelike deckbuilding RPG built with Python and Pygame. Inspired by classic deckbuilders, featuring strategic combat, procedural dungeon crawling, and a custom asset system.

## 🚀 Recent Updates

### New Relics & Mechanics
- **Fire Pendant (Starter)**: The default relic for the hero. Heals 6 HP at the end of every combat.
- **Kryptonite (Uncommon)**: Deals 10% of a boss's maximum HP as damage immediately upon entering a boss fight.
- **Guaranteed First Encounter**: Each run now begins with a **Slime** encounter on Floor 1, featuring custom pixel art.

### Visual Improvements
- **Hero Panel Evolution**: Expanded layout to support longer relic names and custom icons.
- **Asset Integration**: Fully integrated `.png` support for dungeon nodes, relics, and enemy sprites.
- **Localization**: Full support for English and French translations across all items and screens.

## 🛠 Features
- **Procedural Dungeons**: Explore maps with branching paths, events, merchants, and challenging bosses.
- **Strategic Combat**: Manage your energy and deck to defeat a variety of enemies with unique action patterns.
- **Relic System**: Collect powerful items that provide passive bonuses throughout your run.
- **Customizable Assets**: Easily swap or add pixel art by placing `.png` files in the `assets/icons/` directory.

## 🎮 Getting Started

### Prerequisites
- Python 3.10+
- Pygame 2.6.1

### Installation & Execution
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the game:
   ```bash
   python main.py
   ```

## 🎨 Asset Management
The game looks for assets in `assets/icons/`. To use custom art, use the following filenames:
- **Relics**: `Fire_pendant.png`, `kriptonite.png`
- **Enemies**: `Slime.png`
- **Dungeon Nodes**: `node_enemy.png`, `node_elite.png`, `node_boss.png`, `node_chest.png`, `node_merchant.png`, `node_event.png`

Recommended resolution: 32x32 to 64x64 pixels with transparent backgrounds.
