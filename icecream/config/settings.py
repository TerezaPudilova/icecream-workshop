"""
Centrální konfigurace hry - všechny konstanty na jednom místě
"""

import pygame

# =============================================================================
# ZÁKLADNÍ NASTAVENÍ HRY
# =============================================================================

# Rozměry okna
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
WINDOW_TITLE = "Obsluha Zmrzlinárny"

# FPS a časování
FPS = 60
GAME_DURATION_SECONDS = 60

# Pozice pro sestavování objednávek
ASSEMBLY_CENTER_X = WINDOW_WIDTH // 2 - 100
ASSEMBLY_CENTER_Y = WINDOW_HEIGHT // 2 + 50
ASSEMBLY_CENTER = (ASSEMBLY_CENTER_X, ASSEMBLY_CENTER_Y)

# =============================================================================
# BARVY
# =============================================================================

# Základní barvy
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (150, 0, 0)
GREEN = (0, 150, 0)
YELLOW = (255, 255, 0)

# UI barvy
LIGHT_GREEN = (200, 255, 200)
LIGHT_RED = (255, 200, 200)
LIGHT_GRAY = (230, 230, 230)
LIGHT_BLUE = (220, 240, 255)
PANEL_COLOR = (245, 245, 250)

# Barvy pro stav sestavování
ASSEMBLY_NORMAL = (240, 240, 255)
ASSEMBLY_ERROR = (255, 200, 200)

# Gradient barvy pro pozadí
BACKGROUND_INTRO_START = (200, 230, 255)
BACKGROUND_INTRO_END = (255, 255, 255)
BACKGROUND_MENU_START = (255, 200, 220)
BACKGROUND_MENU_END = (255, 240, 200)
BACKGROUND_GAME_OVER_START = (255, 200, 220)
BACKGROUND_GAME_OVER_END = (255, 240, 200)

# =============================================================================
# FONTY A VELIKOSTI
# =============================================================================

# Názvy fontů
FONT_FAMILY = "arial"

# Velikosti fontů
FONT_SIZE_MAIN_TITLE = 48
FONT_SIZE_MENU_TITLE = 72
FONT_SIZE_SUBTITLE = 24
FONT_SIZE_BUTTON = 20
FONT_SIZE_ORDER = 18
FONT_SIZE_SECTION = 18
FONT_SIZE_SMALL = 16
FONT_SIZE_GAME_OVER_TITLE = 60
FONT_SIZE_FINAL_SCORE = 72

# =============================================================================
# ROZMĚRY UI ELEMENTŮ
# =============================================================================

# Rozměry tlačítek
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 30
BUTTON_BORDER_RADIUS = 5

# Rozměry menu tlačítek
MENU_BUTTON_WIDTH = 200
MENU_BUTTON_HEIGHT = 60

# Rozměry finální obrazovky
FINAL_PANEL_WIDTH = 500
FINAL_PANEL_HEIGHT = 200
FINAL_BUTTON_WIDTH = 200
FINAL_BUTTON_HEIGHT = 50
FINAL_BUTTON_SPACING = 20

# Rozměry ingrediencí panelů
CONE_PANEL_WIDTH = 135
CONE_PANEL_HEIGHT = 280
SCOOP_PANEL_WIDTH = 135
SCOOP_PANEL_HEIGHT = 500
PANEL_BORDER_RADIUS = 8

# Rozměry předmětů
DRAGGABLE_ITEM_SIZE = 48
ASSEMBLY_ZONE_WIDTH = 100
ASSEMBLY_ZONE_HEIGHT = 200

# =============================================================================
# POZICE UI ELEMENTŮ
# =============================================================================

# Pozice panelů
CONE_PANEL_X = WINDOW_WIDTH - 300
CONE_PANEL_Y = 20
SCOOP_PANEL_X = WINDOW_WIDTH - 160
SCOOP_PANEL_Y = 20

# Pozice skóre a časomíry
SCORE_PANEL_X = 15
SCORE_PANEL_Y = ASSEMBLY_CENTER_Y - 50
SCORE_PANEL_WIDTH = 200
SCORE_PANEL_HEIGHT = 60

TIMER_PANEL_X = 15
TIMER_PANEL_Y = ASSEMBLY_CENTER_Y - 130
TIMER_PANEL_WIDTH = 200
TIMER_PANEL_HEIGHT = 60

# Pozice nápovědy ovládání
CONTROLS_HELP_X = 10
CONTROLS_HELP_LINE_HEIGHT = 20

# =============================================================================
# HERNÍ MECHANIKY
# =============================================================================

# Zákazníci
MAX_CUSTOMERS_IN_QUEUE = 4
CUSTOMER_SPACING = 60
CUSTOMER_SPEED = 4
CUSTOMER_TARGET_Y = 100
CUSTOMER_TOLERANCE = 3  # Tolerance pro "dorazení" zákazníka

# Časování
NEW_CUSTOMER_DELAY_MIN = 3000  # ms
NEW_CUSTOMER_DELAY_MAX = 5000  # ms
ERROR_DISPLAY_DURATION = 3000  # ms
INTRO_SCREEN_DURATION = 4000   # ms

# Animace
ITEM_HOVER_SCALE = 1.2
ITEM_SCALE_SPEED = 0.15
BOUNCE_SPEED = 0.1

# =============================================================================
# CESTY K ASSETŮM
# =============================================================================

# Základní cesty
ASSETS_DIR = "assets"
ICECREAM_ASSETS_DIR = f"{ASSETS_DIR}/Icecream"
CUSTOMER_ASSETS_DIR = f"{ASSETS_DIR}/Customers"

# Konkrétní soubory
SCOOP_SPRITESHEET = f"{ICECREAM_ASSETS_DIR}/download.png"
CONE_SPRITESHEET = f"{ICECREAM_ASSETS_DIR}/cones.png"
DECORATION_ICECREAM = f"{ICECREAM_ASSETS_DIR}/icecream_uvod_2.png"
CUSTOMER_IMAGE = f"{CUSTOMER_ASSETS_DIR}/Customer1FF.png"

# Záložní obrázky
CHOCOLATE_SCOOP_FALLBACK = f"{ICECREAM_ASSETS_DIR}/cokoladova.png"
VANILLA_SCOOP_FALLBACK = f"{ICECREAM_ASSETS_DIR}/smoulova.png"
CONE_FALLBACK = f"{ICECREAM_ASSETS_DIR}/kornout.png"

# =============================================================================
# HERNÍ DATA
# =============================================================================

# Mapování příchutí (anglicky -> česky)
FLAVOR_NAMES = {
    'raspberry': 'malina',
    'pistachio': 'pistácie', 
    'caramel': 'karamel',
    'hazelnut': 'oříšek',
    'lemon': 'citrón',
    'vanilla': 'vanilka',
    'peach': 'meruňka',
    'strawberry': 'jahoda',
    'chocolate': 'čokoláda'
}

# Mapování kornoutů (anglicky -> česky)
CONE_NAMES = {
    'classic': 'klasický',
    'waffle': 'vafle',
    'short': 'malý',
    'sugar': 'cukrový',
}

# Pořadí příchutí v spritesheet (řádek, sloupec)
SCOOP_SPRITESHEET_LAYOUT = [
    ['raspberry', 'pistachio', 'caramel'],     # řádek 0
    ['hazelnut', 'lemon', 'vanilla'],          # řádek 1  
    ['peach', 'strawberry', 'chocolate']       # řádek 2
]

# Názvy kornoutů v spritesheet (zleva doprava)
CONE_SPRITESHEET_LAYOUT = ['classic', 'waffle', 'short', 'sugar']

# Rozsah počtu kopečků v objednávce
MIN_SCOOPS_PER_ORDER = 1
MAX_SCOOPS_PER_ORDER = 3

# =============================================================================
# SPRITESHEET NASTAVENÍ
# =============================================================================

# Rozměry spritesheetů
SCOOP_SPRITESHEET_COLS = 3
SCOOP_SPRITESHEET_ROWS = 3
CONE_SPRITESHEET_COLS = 4
CONE_SPRITESHEET_ROWS = 1

# Padding pro jednotlivé obrázky (procenta)
SCOOP_PADDING_STANDARD = 0.05
SCOOP_PADDING_MIDDLE_COL_LEFT = 0.06
SCOOP_PADDING_MIDDLE_COL_RIGHT = 0.14
SCOOP_PADDING_RIGHT_COL_LEFT = 0.02
SCOOP_PADDING_RIGHT_COL_RIGHT = 0.08
SCOOP_PADDING_Y = 0.02

CONE_PADDING_CLASSIC_LEFT = 0.15
CONE_PADDING_CLASSIC_RIGHT = 0.03
CONE_PADDING_WAFFLE_LEFT = 0.12
CONE_PADDING_WAFFLE_RIGHT = 0.02
CONE_PADDING_Y = 0.04

# Rozměry dekoračních zmrzlin
DECORATION_ICECREAM_COLS = 5
DECORATION_ICECREAM_SKIP_FIRST = 1  # Přeskočit první zmrzlinu
DECORATION_ICECREAM_FINAL_SIZE = (80, 120)

# =============================================================================
# ANIMACE PLOVOUCÍCH ZMRZLIN
# =============================================================================

# Počet plovoucích zmrzlin na pozadí
FLOATING_ICECREAMS_COUNT = 8

# Rozsahy pro animace
FLOAT_SPEED_MIN = 0.02
FLOAT_SPEED_MAX = 0.05
FLOAT_AMPLITUDE_MIN = 10
FLOAT_AMPLITUDE_MAX = 20
ROTATION_SPEED_MIN = -1
ROTATION_SPEED_MAX = 1
SCALE_MIN = 0.7
SCALE_MAX = 1.3
ALPHA_MIN = 100
ALPHA_MAX = 200

# =============================================================================
# TEXTY A ZPRÁVY
# =============================================================================

# Hlavní texty
MAIN_TITLE = "ZMRZLINÁRNA"
INTRO_TITLE = "Vítejte v Zmrzlinárně!"
INTRO_SUBTITLE = "Připravte se na sladké dobrodružství!"
GAME_OVER_TITLE = "ČAS VYPRŠEL!"
FINAL_SCORE_TITLE = "FINÁLNÍ SKÓRE"

# Texty tlačítek
BUTTON_PLAY = "HRÁT"
BUTTON_DONE = "HOTOVO"
BUTTON_RESET = "ZNOVU"
BUTTON_BACK_TO_MENU = "ZPĚT DO MENU"

# Herní zprávy
ORDER_BUBBLE_TITLE = "AKTUÁLNÍ OBJEDNÁVKA"
ASSEMBLY_ZONE_NORMAL = "SESTAV OBJEDNÁVKU"
ASSEMBLY_ZONE_ERROR = "CHYBNÁ OBJEDNÁVKA!"
QUEUE_TEXT = "Zákazníků ve frontě"

# Nápověda ovládání
CONTROLS_MENU = [
    "OVLÁDÁNÍ:",
    "Enter - Spustit hru",
    "Escape - Ukončit hru"
]

CONTROLS_PLAYING = [
    "OVLÁDÁNÍ:",
    "Enter - Dokončit objednávku", 
    "Mezerník - Reset sestavování",
    "Escape - Návrat do menu"
]

CONTROLS_GAME_OVER_INSTRUCTION = "Použijte myš nebo klávesy Enter/Escape"

# =============================================================================
# FUNKCE PRO INICIALIZACI FONTŮ
# =============================================================================

def init_fonts():
    """
    Inicializuje všechny fonty používané ve hře
    Volá se po pygame.init()
    """
    return {
        'main_title': pygame.font.SysFont(FONT_FAMILY, FONT_SIZE_MAIN_TITLE),
        'menu_title': pygame.font.SysFont(FONT_FAMILY, FONT_SIZE_MENU_TITLE, bold=True),
        'subtitle': pygame.font.SysFont(FONT_FAMILY, FONT_SIZE_SUBTITLE),
        'button': pygame.font.SysFont(FONT_FAMILY, FONT_SIZE_BUTTON),
        'order': pygame.font.SysFont(FONT_FAMILY, FONT_SIZE_ORDER),
        'section': pygame.font.SysFont(FONT_FAMILY, FONT_SIZE_SECTION, bold=True),
        'small': pygame.font.SysFont(FONT_FAMILY, FONT_SIZE_SMALL),
        'game_over_title': pygame.font.SysFont(FONT_FAMILY, FONT_SIZE_GAME_OVER_TITLE, bold=True),
        'final_score': pygame.font.SysFont(FONT_FAMILY, FONT_SIZE_FINAL_SCORE, bold=True),
        'menu_button': pygame.font.SysFont(FONT_FAMILY, 36, bold=True),
        'final_button': pygame.font.SysFont(FONT_FAMILY, 24, bold=True),
        'score': pygame.font.SysFont(FONT_FAMILY, 28, bold=True),
        'timer': pygame.font.SysFont(FONT_FAMILY, 28, bold=True),
    }

# =============================================================================
# POMOCNÉ FUNKCE
# =============================================================================

def get_customer_position(customer_id):
    """Vrátí cílovou pozici zákazníka podle jeho ID"""
    if customer_id == 0:
        return WINDOW_WIDTH // 2 - 100, CUSTOMER_TARGET_Y
    elif customer_id == 1:
        return WINDOW_WIDTH // 2 - 100 - 3 * CUSTOMER_SPACING, CUSTOMER_TARGET_Y
    else:
        return (WINDOW_WIDTH // 2 - 100 - 3 * CUSTOMER_SPACING - 
                (customer_id - 1) * CUSTOMER_SPACING, CUSTOMER_TARGET_Y)

def get_ingredient_position(item_type, index):
    """Vrátí pozici ingredience podle typu a indexu"""
    if item_type == "cone":
        return CONE_PANEL_X - 290, CONE_PANEL_Y + 30 + (index * 60)
    elif item_type == "scoop":
        return SCOOP_PANEL_X - 150, SCOOP_PANEL_Y + 30 + (index * 50)
    return 0, 0

def get_assembly_item_position(item_type, scoop_count=0):
    """Vrátí pozici předmětu v assembly zóně"""
    if item_type == "cone":
        return ASSEMBLY_CENTER_X, ASSEMBLY_CENTER_Y + 20
    else:  # scoop
        return ASSEMBLY_CENTER_X, ASSEMBLY_CENTER_Y - scoop_count * 25