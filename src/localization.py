"""
Localization / i18n system.
Provides a global LANG setting and a t() function to get translated strings.
"""

# Supported languages
LANG_EN = "en"
LANG_FR = "fr"

# Active language (mutable global)
_current_lang = LANG_EN


def set_language(lang: str):
    global _current_lang
    if lang in (LANG_EN, LANG_FR):
        _current_lang = lang


def get_language() -> str:
    return _current_lang


def t(key: str) -> str:
    """Return the translated string for the given key in the current language."""
    strings = STRINGS.get(_current_lang, STRINGS[LANG_EN])
    return strings.get(key, STRINGS[LANG_EN].get(key, key))


# ─────────────────────────────────────────────────────────────────────────────
# String Table
# ─────────────────────────────────────────────────────────────────────────────

STRINGS = {
    LANG_EN: {
        # ── Main Menu ──
        "menu.title_1":       "GAME",
        "menu.title_2":       "DECK",
        "menu.title_3":       "RPG",
        "menu.subtitle":      "A Roguelike Card Dungeon Crawler",
        "menu.new_run":       "▶  NEW RUN",
        "menu.settings":      "SETTINGS",
        "menu.quit":          "QUIT",
        "menu.version":       "v1.0",

        # ── Settings ──
        "settings.title":     "SETTINGS",
        "settings.language":  "Language",
        "settings.back":      "← Back",
        "settings.lang_en":   "English",
        "settings.lang_fr":   "Français",

        # ── Map ──
        "map.title":          "DUNGEON MAP",
        "map.floor":          "Floor",
        "map.gold":           "Gold:",
        "map.deck":           "Deck:",
        "map.cards":          "cards",
        "map.current":        "► CURRENT",
        "map.done":           "✓ Done",
        "map.enter":          "Enter",

        # ── Node types ──
        "node.enemy":         "ENEMY",
        "node.elite":         "ELITE",
        "node.boss":          "BOSS",
        "node.chest":         "CHEST",
        "node.merchant":      "MERCHANT",
        "node.event":         "EVENT",

        # ── Combat ──
        "combat.your_turn":   "YOUR TURN",
        "combat.enemy_turn":  "ENEMY TURN...",
        "combat.end_turn":    "END TURN",
        "combat.draw":        "Draw:",
        "combat.discard":     "Discard:",
        "combat.target_hint": "Click an enemy to target",
        "combat.played":      "Played:",
        "combat.log_title":   "Combat Log",

        # ── Card types ──
        "card.attack":        "Attack",
        "card.skill":         "Skill",
        "card.power":         "Power",

        # ── Card rarities ──
        "rarity.starter":     "Starter",
        "rarity.common":      "Common",
        "rarity.uncommon":    "Uncommon",
        "rarity.rare":        "Rare",

        # ── Card reward ──
        "reward.title":       "⚔  CHOOSE A CARD  ⚔",
        "reward.gold_earned": "Gold earned:",
        "reward.add_hint":    "Click to add to deck",
        "reward.skip":        "Skip",

        # ── Merchant ──
        "merchant.title":     "🛒  MERCHANT",
        "merchant.gold":      "Gold:",
        "merchant.remove":    "Remove Card",
        "merchant.leave":     "Leave",
        "merchant.bought":    "Bought",
        "merchant.no_gold":   "Not enough gold!",
        "merchant.deck_small":"Deck too small!",
        "merchant.removed":   "Removed",

        # ── Chest ──
        "chest.title":        "📦  TREASURE CHEST",
        "chest.gold":         "Gold: +",
        "chest.found_relic":  "You also found a relic:",
        "chest.take_both":    "Take Relic & Gold",
        "chest.take_gold":    "Take Gold Only",

        # ── Event ──
        "event.title_prefix": "❓  ",
        "event.what_do":      "What do you do?",
        "event.continue":     "Continue",

        # ── Game Over ──
        "gameover.title":     "YOU DIED",
        "gameover.floor":     "Floor Reached:",
        "gameover.kills":     "Enemies Slain:",
        "gameover.deck":      "Cards in Deck:",
        "gameover.relics":    "Relics:",
        "gameover.new_run":   "▶  NEW RUN",
        "gameover.menu":      "Main Menu",

        # ── Hero panel ──
        "hero.hp":            "HP",

        # ── Status effects ──
        "status.Strength":    "Strength",
        "status.Dexterity":   "Dexterity",
        "status.Weak":        "Weak",
        "status.Vulnerable":  "Vulnerable",
        "status.Burn":        "Burn",
        "status.Poison":      "Poison",
        "status.Regeneration":"Regeneration",
        "status.Ritual":      "Ritual",
        "status.Thorns":      "Thorns",

        # ── New Relics ──
        "relic.name.Kryptonite":    "Kryptonite",
        "relic.desc.Kryptonite":    "Deal 10% Boss HP on entry.",
        "relic.name.Fire Pendant":  "Fire Pendant",
        "relic.desc.Fire Pendant":  "Heal 6 HP at end of combat.",

        # ── Action Intents ──
        "intent.attack":      "Attack",
        "intent.defend":      "Defend",
        "intent.buff":        "Buff",
        "intent.debuff":      "Debuff",

        # ── Enemy names ──
        "enemy.name.Cultist":         "Cultist",
        "enemy.name.Jaw Worm":        "Jaw Worm",
        "enemy.name.Louse":           "Louse",
        "enemy.name.Fungal Spore":    "Fungal Spore",
        "enemy.name.Slime":           "Slime",
        "enemy.name.Gremlin Nob":     "Gremlin Nob",
        "enemy.name.Lagavulin":       "Lagavulin",
        "enemy.name.Sentry":          "Sentry",
        "enemy.name.Blue Slaver":     "Blue Slaver",
        "enemy.name.Red Slaver":      "Red Slaver",
        "enemy.name.Writhing Mass":   "Writhing Mass",
        "enemy.name.Repulsor":        "Repulsor",
        "enemy.name.Nemesis":         "Nemesis",
        "enemy.name.Deca":            "Deca",
        "enemy.name.The Guardian":    "The Guardian",
        "enemy.name.Hexaghost":       "Hexaghost",
        "enemy.name.Slime Boss":      "Slime Boss",
        "enemy.name.Time Eater":      "Time Eater",

        # ── Event content ──
        "event.name.Ancient Shrine":      "Ancient Shrine",
        "event.desc.Ancient Shrine":      "You find an ancient shrine. Strange runes glow faintly.",
        "event.choice.Ancient Shrine.0":  "Pray (Heal 25% HP)",
        "event.choice.Ancient Shrine.1":  "Offer blood (Lose 10% HP, gain 50 gold)",
        "event.choice.Ancient Shrine.2":  "Leave",

        "event.name.Mysterious Merchant":  "Mysterious Merchant",
        "event.desc.Mysterious Merchant":  "A hooded figure offers you a deal.",
        "event.choice.Mysterious Merchant.0": "Buy strength (+1 Strength, -50 gold)",
        "event.choice.Mysterious Merchant.1": "Ignore and leave",

        "event.name.Forgotten Library":    "Forgotten Library",
        "event.desc.Forgotten Library":    "Dusty tomes line the walls. One book glows.",
        "event.choice.Forgotten Library.0": "Read the book (Add a random card)",
        "event.choice.Forgotten Library.1": "Burn a book (Remove a random card)",
        "event.choice.Forgotten Library.2": "Leave",

        "event.name.Treasure Room":        "Treasure Room",
        "event.desc.Treasure Room":        "A small chest sits in the center of the room.",
        "event.choice.Treasure Room.0":    "Open it (Gain 75 gold)",
        "event.choice.Treasure Room.1":    "Leave it (Suspicious...)",

        "event.name.Cursed Tome":          "Cursed Tome",
        "event.desc.Cursed Tome":          "A dark tome whispers your name.",
        "event.choice.Cursed Tome.0":      "Read it (Gain 5 Max HP, lose 10 gold)",
        "event.choice.Cursed Tome.1":      "Burn it (Gain 30 gold)",
        "event.choice.Cursed Tome.2":      "Ignore",

        "event.name.Bandit Ambush":        "Bandit Ambush",
        "event.desc.Bandit Ambush":        "Bandits jump out! They demand your gold.",
        "event.choice.Bandit Ambush.0":    "Pay them (Lose 50 gold)",
        "event.choice.Bandit Ambush.1":    "Fight back (Lose 15 HP)",

        "event.name.Healing Fountain":     "Healing Fountain",
        "event.desc.Healing Fountain":     "A crystal-clear fountain bubbles with magical water.",
        "event.choice.Healing Fountain.0": "Drink (Heal 25% HP)",
        "event.choice.Healing Fountain.1": "Fill your flask (Gain 5 Max HP)",

        "event.name.Wandering Merchant":   "Wandering Merchant",
        "event.desc.Wandering Merchant":   "A merchant lost in the dungeon offers a quick deal.",
        "event.choice.Wandering Merchant.0":"Buy a random card (75 gold)",
        "event.choice.Wandering Merchant.1":"Leave",

        # ── Card names ──
        "card.name.Strike":           "Strike",
        "card.name.Defend":           "Defend",
        "card.name.Bash":             "Bash",
        "card.name.Heavy Blade":      "Heavy Blade",
        "card.name.Twin Strike":      "Twin Strike",
        "card.name.Body Slam":        "Body Slam",
        "card.name.Pommel Strike":    "Pommel Strike",
        "card.name.Iron Wave":        "Iron Wave",
        "card.name.Cleave":           "Cleave",
        "card.name.Thunderclap":      "Thunderclap",
        "card.name.Headbutt":         "Headbutt",
        "card.name.Wild Strike":      "Wild Strike",
        "card.name.Sword Boomerang":  "Sword Boomerang",
        "card.name.Perfected Strike": "Perfected Strike",
        "card.name.Shrug It Off":     "Shrug It Off",
        "card.name.True Grit":        "True Grit",
        "card.name.Armaments":        "Armaments",
        "card.name.Seeing Red":       "Seeing Red",
        "card.name.Burning Pact":     "Burning Pact",
        "card.name.Bloodletting":     "Bloodletting",
        "card.name.Whirlwind":        "Whirlwind",
        "card.name.Fiend Fire":       "Fiend Fire",
        "card.name.Feed":             "Feed",
        "card.name.Reaper":           "Reaper",
        "card.name.Spot Weakness":    "Spot Weakness",
        "card.name.Battle Trance":    "Battle Trance",
        "card.name.Second Wind":      "Second Wind",
        "card.name.Entrench":         "Entrench",
        "card.name.Flame Barrier":    "Flame Barrier",
        "card.name.Offering":         "Offering",
        "card.name.Sentinel":         "Sentinel",
        "card.name.Inflame":          "Inflame",
        "card.name.Flex":             "Flex",
        "card.name.Dark Embrace":     "Dark Embrace",
        "card.name.Feel No Pain":     "Feel No Pain",
        "card.name.Metallicize":      "Metallicize",
        "card.name.Brutality":        "Brutality",
        "card.name.Berserk":          "Berserk",
        "card.name.Limit Break":      "Limit Break",
        "card.name.Impervious":       "Impervious",
        "card.name.Barricade":        "Barricade",
        "card.name.Juggernaut":       "Juggernaut",
        "card.name.Corruption":       "Corruption",
        "card.name.Combust":          "Combust",
        "card.name.Evolve":           "Evolve",
        "card.name.Wound":            "Wound",

        # ── Card descriptions ──
        "card.desc.Strike":           "Deal 6 damage.",
        "card.desc.Defend":           "Gain 5 Block.",
        "card.desc.Bash":             "Deal 8 damage. Apply 2 Vulnerable.",
        "card.desc.Heavy Blade":      "Deal 14 damage.",
        "card.desc.Twin Strike":      "Deal 5 damage twice.",
        "card.desc.Body Slam":        "Deal damage equal to your Block.",
        "card.desc.Pommel Strike":    "Deal 9 damage. Draw 1 card.",
        "card.desc.Iron Wave":        "Deal 5 damage. Gain 5 Block.",
        "card.desc.Cleave":           "Deal 8 damage to ALL enemies.",
        "card.desc.Thunderclap":      "Deal 4 damage to ALL. Apply 1 Vulnerable.",
        "card.desc.Headbutt":         "Deal 9 damage. Put top discard on draw pile.",
        "card.desc.Wild Strike":      "Deal 12 damage. Add a Wound to draw pile.",
        "card.desc.Sword Boomerang":  "Deal 3 damage 3 times to random enemies.",
        "card.desc.Perfected Strike": "Deal 6+2 damage per Strike in your deck.",
        "card.desc.Shrug It Off":     "Gain 8 Block. Draw 1 card.",
        "card.desc.True Grit":        "Gain 7 Block. Exhaust a random hand card.",
        "card.desc.Armaments":        "Gain 5 Block. Draw 1 card.",
        "card.desc.Seeing Red":       "Gain 2 Energy.",
        "card.desc.Burning Pact":     "Exhaust a card. Draw 2 cards.",
        "card.desc.Bloodletting":     "Lose 3 HP. Gain 2 Energy.",
        "card.desc.Whirlwind":        "Deal 5 damage to ALL enemies X times (X=Energy).",
        "card.desc.Fiend Fire":       "Exhaust hand. Deal 7 damage per card.",
        "card.desc.Feed":             "Deal 10 damage. If fatal, gain 3 Max HP.",
        "card.desc.Reaper":           "Deal 4 damage to ALL. Heal HP equal to damage.",
        "card.desc.Spot Weakness":    "If enemy intends to attack, gain 3 Strength.",
        "card.desc.Battle Trance":    "Draw 3 cards.",
        "card.desc.Second Wind":      "Exhaust non-Attack cards. Gain 5 Block each.",
        "card.desc.Entrench":         "Double your Block.",
        "card.desc.Flame Barrier":    "Gain 12 Block. Gain 4 Thorns.",
        "card.desc.Offering":         "Lose 6 HP. Gain 2 Energy. Draw 3 cards.",
        "card.desc.Sentinel":         "Gain 13 Block.",
        "card.desc.Inflame":          "Gain 2 Strength.",
        "card.desc.Flex":             "Gain 2 Strength.",
        "card.desc.Dark Embrace":     "Whenever you Exhaust, draw 1 card.",
        "card.desc.Feel No Pain":     "Whenever you Exhaust, gain 3 Block.",
        "card.desc.Metallicize":      "At end of turn, gain 3 Block.",
        "card.desc.Brutality":        "At start of turn, lose 1 HP and draw 1 card.",
        "card.desc.Berserk":          "Gain 2 Vulnerable. At start of turn, gain 1 Energy.",
        "card.desc.Limit Break":      "Double your Strength.",
        "card.desc.Impervious":       "Gain 30 Block.",
        "card.desc.Barricade":        "Block no longer resets at start of turn.",
        "card.desc.Juggernaut":       "Whenever you gain Block, deal 5 damage to a random enemy.",
        "card.desc.Corruption":       "Skills cost 0. Whenever you play a Skill, Exhaust it.",
        "card.desc.Combust":          "At end of turn, lose 1 HP and deal 5 damage to ALL.",
        "card.desc.Evolve":           "Whenever you receive a status card, draw 1 card.",
        "card.desc.Wound":            "Unplayable. Clogs your hand.",

        # ── Relic descriptions ──
        "relic.desc.Burning Blood":        "Heal 6 HP at end of each combat.",
        "relic.desc.Anchor":               "Start each combat with 10 Block.",
        "relic.desc.Bag of Preparation":   "Draw 2 extra cards at the start of combat.",
        "relic.desc.Red Skull":            "While at or below 50% HP, gain 3 Strength.",
        "relic.desc.Vajra":                "Gain 1 Strength at the start of each combat.",
        "relic.desc.Odd Mushroom":         "When Weakened, gain 3 Max HP.",
        "relic.desc.Lantern":              "Gain 1 Energy on the first turn of combat.",
        "relic.desc.Tiny Chest":           "Every 4th room is a Chest.",
        "relic.desc.Coffee Dripper":       "Gain 1 Energy each turn.",
        "relic.desc.Philosopher's Stone":  "Gain 1 Energy each turn. Enemies gain 1 Strength.",
        "relic.desc.Akabeko":              "First Attack each combat deals 8 extra damage.",
        "relic.desc.Centennial Puzzle":    "First time you lose HP each combat, draw 3 cards.",
        "relic.desc.Magic Flower":         "Healing is 50% more effective.",
    },

    LANG_FR: {
        # ── Main Menu ──
        "menu.title_1":       "GAME",
        "menu.title_2":       "DECK",
        "menu.title_3":       "RPG",
        "menu.subtitle":      "Un Donjon Roguelike de Cartes",
        "menu.new_run":       "▶  NOUVELLE PARTIE",
        "menu.settings":      "PARAMÈTRES",
        "menu.quit":          "QUITTER",
        "menu.version":       "v1.0",

        # ── Settings ──
        "settings.title":     "PARAMÈTRES",
        "settings.language":  "Langue",
        "settings.back":      "← Retour",
        "settings.lang_en":   "English",
        "settings.lang_fr":   "Français",

        # ── Map ──
        "map.title":          "CARTE DU DONJON",
        "map.floor":          "Étage",
        "map.gold":           "Or :",
        "map.deck":           "Deck :",
        "map.cards":          "cartes",
        "map.current":        "► ACTUEL",
        "map.done":           "✓ Fait",
        "map.enter":          "Entrer",

        # ── Node types ──
        "node.enemy":         "ENNEMI",
        "node.elite":         "ÉLITE",
        "node.boss":          "BOSS",
        "node.chest":         "COFFRE",
        "node.merchant":      "MARCHAND",
        "node.event":         "ÉVÉNEMENT",

        # ── Combat ──
        "combat.your_turn":   "VOTRE TOUR",
        "combat.enemy_turn":  "TOUR ENNEMI...",
        "combat.end_turn":    "FIN DU TOUR",
        "combat.draw":        "Pioche :",
        "combat.discard":     "Défausse :",
        "combat.target_hint": "Cliquez sur un ennemi pour cibler",
        "combat.played":      "Joué :",
        "combat.log_title":   "Journal de Combat",

        # ── Card types ──
        "card.attack":        "Attaque",
        "card.skill":         "Compétence",
        "card.power":         "Pouvoir",

        # ── Card rarities ──
        "rarity.starter":     "Départ",
        "rarity.common":      "Commun",
        "rarity.uncommon":    "Peu Commun",
        "rarity.rare":        "Rare",

        # ── Card reward ──
        "reward.title":       "⚔  CHOISISSEZ UNE CARTE  ⚔",
        "reward.gold_earned": "Or gagné :",
        "reward.add_hint":    "Cliquez pour ajouter au deck",
        "reward.skip":        "Passer",

        # ── Merchant ──
        "merchant.title":     "🛒  MARCHAND",
        "merchant.gold":      "Or :",
        "merchant.remove":    "Retirer une carte",
        "merchant.leave":     "Partir",
        "merchant.bought":    "Acheté",
        "merchant.no_gold":   "Pas assez d'or !",
        "merchant.deck_small":"Deck trop petit !",
        "merchant.removed":   "Retiré",

        # ── Chest ──
        "chest.title":        "📦  COFFRE AU TRÉSOR",
        "chest.gold":         "Or : +",
        "chest.found_relic":  "Vous avez aussi trouvé une relique :",
        "chest.take_both":    "Prendre Relique & Or",
        "chest.take_gold":    "Prendre l'Or seulement",

        # ── Event ──
        "event.title_prefix": "❓  ",
        "event.what_do":      "Que faites-vous ?",
        "event.continue":     "Continuer",

        # ── Game Over ──
        "gameover.title":     "VOUS ÊTES MORT",
        "gameover.floor":     "Étage atteint :",
        "gameover.kills":     "Ennemis tués :",
        "gameover.deck":      "Cartes dans le deck :",
        "gameover.relics":    "Reliques :",
        "gameover.new_run":   "▶  NOUVELLE PARTIE",
        "gameover.menu":      "Menu Principal",

        # ── Hero panel ──
        "hero.hp":            "PV",

        # ── Status effects ──
        "status.Strength":    "Force",
        "status.Dexterity":   "Dextérité",
        "status.Weak":        "Affaibli",
        "status.Vulnerable":  "Vulnérable",
        "status.Burn":        "Brûlure",
        "status.Poison":      "Poison",
        "status.Regeneration":"Régénération",
        "status.Ritual":      "Rituel",
        "status.Thorns":      "Épines",

        # ── Nouveaux Reliques ──
        "relic.name.Kryptonite":    "Kryptonite",
        "relic.desc.Kryptonite":    "Inflige 10% des PV du Boss à l'entrée.",
        "relic.name.Fire Pendant":  "Pendentif de Feu",
        "relic.desc.Fire Pendant":  "Soigne 6 PV à la fin du combat.",

        # ── Action Intents ──
        "intent.attack":      "Attaque",
        "intent.defend":      "Défense",
        "intent.buff":        "Bonus",
        "intent.debuff":      "Malus",

        # ── Enemy names ──
        "enemy.name.Cultist":         "Cultiste",
        "enemy.name.Jaw Worm":        "Ver Mâchoire",
        "enemy.name.Louse":           "Pou",
        "enemy.name.Fungal Spore":    "Spore Fongique",
        "enemy.name.Slime":           "Gluant",
        "enemy.name.Gremlin Nob":     "Gremlin Nob",
        "enemy.name.Lagavulin":       "Lagavulin",
        "enemy.name.Sentry":          "Sentinelle",
        "enemy.name.Blue Slaver":     "Esclavagiste Bleu",
        "enemy.name.Red Slaver":      "Esclavagiste Rouge",
        "enemy.name.Writhing Mass":   "Masse Gigotante",
        "enemy.name.Repulsor":        "Répulseur",
        "enemy.name.Nemesis":         "Némésis",
        "enemy.name.Deca":            "Deca",
        "enemy.name.The Guardian":    "Le Gardien",
        "enemy.name.Hexaghost":       "Hexaghost",
        "enemy.name.Slime Boss":      "Boss Gluant",
        "enemy.name.Time Eater":      "Mangeur de Temps",

        # ── Event content ──
        "event.name.Ancient Shrine":      "Ancien Sanctuaire",
        "event.desc.Ancient Shrine":      "Vous trouvez un ancien sanctuaire. Des runes étranges brillent faiblement.",
        "event.choice.Ancient Shrine.0":  "Prier (Soigne 25% PV)",
        "event.choice.Ancient Shrine.1":  "Offrir son sang (Perd 10% PV, gagne 50 or)",
        "event.choice.Ancient Shrine.2":  "Partir",

        "event.name.Mysterious Merchant":  "Marchand Mystérieux",
        "event.desc.Mysterious Merchant":  "Une figure encapuchonnée vous propose un marché.",
        "event.choice.Mysterious Merchant.0": "Acheter force (+1 Force, -50 or)",
        "event.choice.Mysterious Merchant.1": "Ignorer et partir",

        "event.name.Forgotten Library":    "Bibliothèque Oubliée",
        "event.desc.Forgotten Library":    "Des tomes poussiéreux tapissent les murs. Un livre brille.",
        "event.choice.Forgotten Library.0": "Lire le livre (Ajouter une carte aléatoire)",
        "event.choice.Forgotten Library.1": "Brûler un livre (Retirer une carte aléatoire)",
        "event.choice.Forgotten Library.2": "Partir",

        "event.name.Treasure Room":        "Salle au Trésor",
        "event.desc.Treasure Room":        "Un petit coffre trône au centre de la pièce.",
        "event.choice.Treasure Room.0":    "L'ouvrir (Gagne 75 or)",
        "event.choice.Treasure Room.1":    "Le laisser (Suspect...)",

        "event.name.Cursed Tome":          "Tome Maudit",
        "event.desc.Cursed Tome":          "Un tome sombre murmure votre nom.",
        "event.choice.Cursed Tome.0":      "Le lire (Gagne 5 PV Max, perd 10 or)",
        "event.choice.Cursed Tome.1":      "Le brûler (Gagne 30 or)",
        "event.choice.Cursed Tome.2":      "Ignorer",

        "event.name.Bandit Ambush":        "Embuscade de Bandits",
        "event.desc.Bandit Ambush":        "Des bandits surgissent ! Ils réclament votre or.",
        "event.choice.Bandit Ambush.0":    "Les payer (Perd 50 or)",
        "event.choice.Bandit Ambush.1":    "Se défendre (Perd 15 PV)",

        "event.name.Healing Fountain":     "Fontaine Curative",
        "event.desc.Healing Fountain":     "Une fontaine cristalline bouillonne d'eau magique.",
        "event.choice.Healing Fountain.0": "Boire (Soigne 25% PV)",
        "event.choice.Healing Fountain.1": "Remplir sa gourde (Gagne 5 PV Max)",

        "event.name.Wandering Merchant":   "Marchand Errant",
        "event.desc.Wandering Merchant":   "Un marchand égaré dans le donjon propose une affaire rapide.",
        "event.choice.Wandering Merchant.0":"Acheter une carte aléatoire (75 or)",
        "event.choice.Wandering Merchant.1":"Partir",

        # ── Card names ──
        "card.name.Strike":           "Frappe",
        "card.name.Defend":           "Défense",
        "card.name.Bash":             "Coup de Pommeau",
        "card.name.Heavy Blade":      "Lame Lourde",
        "card.name.Twin Strike":      "Frappe Double",
        "card.name.Body Slam":        "Coup de Corps",
        "card.name.Pommel Strike":    "Frappe de Pommeau",
        "card.name.Iron Wave":        "Vague de Fer",
        "card.name.Cleave":           "Enchaînement",
        "card.name.Thunderclap":      "Coup de Tonnerre",
        "card.name.Headbutt":         "Coup de Tête",
        "card.name.Wild Strike":      "Frappe Sauvage",
        "card.name.Sword Boomerang":  "Épée Boomerang",
        "card.name.Perfected Strike": "Frappe Parfaite",
        "card.name.Shrug It Off":     "Indifférence",
        "card.name.True Grit":        "Sang-froid",
        "card.name.Armaments":        "Armement",
        "card.name.Seeing Red":       "Voir Rouge",
        "card.name.Burning Pact":     "Pacte de Feu",
        "card.name.Bloodletting":     "Saignée",
        "card.name.Whirlwind":        "Tourbillon",
        "card.name.Fiend Fire":       "Feu Infernal",
        "card.name.Feed":             "Nourrir",
        "card.name.Reaper":           "Faucheuse",
        "card.name.Spot Weakness":    "Déceler la Faiblesse",
        "card.name.Battle Trance":    "Transe de Combat",
        "card.name.Second Wind":      "Second Souffle",
        "card.name.Entrench":         "Retranchement",
        "card.name.Flame Barrier":    "Barrière de Flammes",
        "card.name.Offering":         "Offrande",
        "card.name.Sentinel":         "Sentinelle",
        "card.name.Inflame":          "Enflammer",
        "card.name.Flex":             "Contracter",
        "card.name.Dark Embrace":     "Étreinte Sombre",
        "card.name.Feel No Pain":     "Insensibilité",
        "card.name.Metallicize":      "Plastron de Métal",
        "card.name.Brutality":        "Brutalité",
        "card.name.Berserk":          "Berserk",
        "card.name.Limit Break":      "Transcendance",
        "card.name.Impervious":       "Invulnérable",
        "card.name.Barricade":        "Barricade",
        "card.name.Juggernaut":       "Juggernaut",
        "card.name.Corruption":       "Corruption",
        "card.name.Combust":          "Combustion",
        "card.name.Evolve":           "Évoluer",
        "card.name.Wound":            "Blessure",

        # ── Card descriptions ──
        "card.desc.Strike":           "Inflige 6 dégâts.",
        "card.desc.Defend":           "Gagne 5 Bouclier.",
        "card.desc.Bash":             "Inflige 8 dégâts. Applique 2 Vulnérable.",
        "card.desc.Heavy Blade":      "Inflige 14 dégâts.",
        "card.desc.Twin Strike":      "Inflige 5 dégâts deux fois.",
        "card.desc.Body Slam":        "Inflige des dégâts égaux à votre Bouclier.",
        "card.desc.Pommel Strike":    "Inflige 9 dégâts. Piochez 1 carte.",
        "card.desc.Iron Wave":        "Inflige 5 dégâts. Gagne 5 Bouclier.",
        "card.desc.Cleave":           "Inflige 8 dégâts à TOUS les ennemis.",
        "card.desc.Thunderclap":      "Inflige 4 dégâts à TOUS. Applique 1 Vulnérable.",
        "card.desc.Headbutt":         "Inflige 9 dégâts. Remet la défausse sur la pioche.",
        "card.desc.Wild Strike":      "Inflige 12 dégâts. Ajoute une Blessure à la pioche.",
        "card.desc.Sword Boomerang":  "Inflige 3 dégâts 3 fois à des ennemis aléatoires.",
        "card.desc.Perfected Strike": "Inflige 6+2 dégâts par Frappe dans votre deck.",
        "card.desc.Shrug It Off":     "Gagne 8 Bouclier. Piochez 1 carte.",
        "card.desc.True Grit":        "Gagne 7 Bouclier. Épuise une carte aléatoire.",
        "card.desc.Armaments":        "Gagne 5 Bouclier. Piochez 1 carte.",
        "card.desc.Seeing Red":       "Gagne 2 Énergie.",
        "card.desc.Burning Pact":     "Épuise une carte. Piochez 2 cartes.",
        "card.desc.Bloodletting":     "Perd 3 PV. Gagne 2 Énergie.",
        "card.desc.Whirlwind":        "Inflige 5 dégâts à TOUS X fois (X=Énergie).",
        "card.desc.Fiend Fire":       "Épuise la main. Inflige 7 dégâts par carte.",
        "card.desc.Feed":             "Inflige 10 dégâts. Si fatal, gagne 3 PV max.",
        "card.desc.Reaper":           "Inflige 4 dégâts à TOUS. Soigne les dégâts infligés.",
        "card.desc.Spot Weakness":    "Si l'ennemi attaque, gagne 3 Force.",
        "card.desc.Battle Trance":    "Piochez 3 cartes.",
        "card.desc.Second Wind":      "Épuise les non-Attaques. Gagne 5 Bouclier chacune.",
        "card.desc.Entrench":         "Double votre Bouclier.",
        "card.desc.Flame Barrier":    "Gagne 12 Bouclier. Gagne 4 Épines.",
        "card.desc.Offering":         "Perd 6 PV. Gagne 2 Énergie. Piochez 3 cartes.",
        "card.desc.Sentinel":         "Gagne 13 Bouclier.",
        "card.desc.Inflame":          "Gagne 2 Force.",
        "card.desc.Flex":             "Gagne 2 Force.",
        "card.desc.Dark Embrace":     "Chaque Épuisement : piochez 1 carte.",
        "card.desc.Feel No Pain":     "Chaque Épuisement : gagne 3 Bouclier.",
        "card.desc.Metallicize":      "Fin de tour : gagne 3 Bouclier.",
        "card.desc.Brutality":        "Début de tour : perd 1 PV et pioche 1 carte.",
        "card.desc.Berserk":          "Gagne 2 Vulnérable. Début de tour : gagne 1 Énergie.",
        "card.desc.Limit Break":      "Double votre Force.",
        "card.desc.Impervious":       "Gagne 30 Bouclier.",
        "card.desc.Barricade":        "Le Bouclier ne se réinitialise plus en début de tour.",
        "card.desc.Juggernaut":       "Chaque Bouclier gagné : inflige 5 dégâts à un ennemi aléatoire.",
        "card.desc.Corruption":       "Les Compétences coûtent 0. Elles s'épuisent.",
        "card.desc.Combust":          "Fin de tour : perd 1 PV et inflige 5 dégâts à TOUS.",
        "card.desc.Evolve":           "Chaque carte de statut reçue : piochez 1 carte.",
        "card.desc.Wound":            "Non jouable. Encombre votre main.",

        # ── Relic descriptions ──
        "relic.desc.Burning Blood":        "Soigne 6 PV à la fin de chaque combat.",
        "relic.desc.Anchor":               "Commence chaque combat avec 10 Bouclier.",
        "relic.desc.Bag of Preparation":   "Piochez 2 cartes supplémentaires au début du combat.",
        "relic.desc.Red Skull":            "Sous 50% PV, gagne 3 Force.",
        "relic.desc.Vajra":                "Gagne 1 Force au début de chaque combat.",
        "relic.desc.Odd Mushroom":         "Quand Affaibli, gagne 3 PV max.",
        "relic.desc.Lantern":              "Gagne 1 Énergie au premier tour du combat.",
        "relic.desc.Tiny Chest":           "Toutes les 4 salles est un Coffre.",
        "relic.desc.Coffee Dripper":       "Gagne 1 Énergie chaque tour.",
        "relic.desc.Philosopher's Stone":  "Gagne 1 Énergie chaque tour. Les ennemis gagnent 1 Force.",
        "relic.desc.Akabeko":              "La première Attaque de chaque combat inflige 8 dégâts supplémentaires.",
        "relic.desc.Centennial Puzzle":    "Première perte de PV du combat : piochez 3 cartes.",
        "relic.desc.Magic Flower":         "Les soins sont 50% plus efficaces.",
    },
}
