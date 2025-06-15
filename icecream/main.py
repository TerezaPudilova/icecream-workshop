import pygame
import sys
import random
import math

# Inicializace Pygame
pygame.init()

# Nastavení velikosti okna - zvětšeno pro lepší rozhraní
WIDTH, HEIGHT = 1200, 700  
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Obsluha Zmrzlinárny")

ASSEMBLY_CENTER = (WIDTH // 2 - 100, HEIGHT // 2 + 50)

# FPS a časovač
clock = pygame.time.Clock()
FPS = 60

# Barvy
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 150, 0)
RED = (150, 0, 0)
LIGHT_GREEN = (200, 255, 200)
LIGHT_RED = (255, 200, 200)
LIGHT_GRAY = (230, 230, 230)
LIGHT_BLUE = (220, 240, 255)
ASSEMBLY_NORMAL = (240, 240, 255)
ASSEMBLY_ERROR = (255, 200, 200)
YELLOW = (255, 255, 0)
PANEL_COLOR = (245, 245, 250)

# Fonty
font = pygame.font.SysFont("arial", 48)
small_font = pygame.font.SysFont("arial", 16)
button_font = pygame.font.SysFont("arial", 20)
order_font = pygame.font.SysFont("arial", 18)
section_font = pygame.font.SysFont("arial", 18, bold=True)

# NOVÉ: Načtení zmrzlin pro dekoraci
def load_icecream_decoration():
    """Načte obrázek zmrzlin a rozřeže ho na jednotlivé kornouty se zmrzlinou"""
    try:
        # Načtení obrázku s 5 zmrzlinami v řadě
        icecream_sheet = pygame.image.load("icecream/assets/Icecream/icecream_uvod_2.png").convert_alpha()  # Název vašeho obrázku
        
        sheet_width = icecream_sheet.get_width()
        sheet_height = icecream_sheet.get_height()
        
        # UPRAVENO: Lepší výpočet velikosti jedné zmrzliny s paddingem
        icecream_width = sheet_width // 5
        icecream_height = sheet_height
        
        # NOVÉ: Padding pro lepší oříznutí (odstraní přečuhující části)
        padding_x = int(icecream_width * 0.05)  # 5% padding zleva a zprava
        padding_y = int(icecream_height * 0.02)  # 2% padding shora a zdola
        
        icecreams = []
        
        # UPRAVENO: Rozřezání na 4 zmrzliny (vynecháváme první - nejvíc nalevo)
        for i in range(1, 5):  # Začínáme od indexu 1 místo 0
            # NOVÉ: Aplikace paddingu pro lepší oříznutí
            rect = pygame.Rect(
                i * icecream_width + padding_x, 
                padding_y, 
                icecream_width - 2 * padding_x, 
                icecream_height - 2 * padding_y
            )
            icecream_surface = icecream_sheet.subsurface(rect)
            # Změna velikosti pro lepší použití v UI
            scaled_icecream = pygame.transform.scale(icecream_surface, (80, 120))
            icecreams.append(scaled_icecream)
                
        return icecreams
        
    except pygame.error:
        print("Nepodařilo se načíst obrázek zmrzlin pro dekoraci, používám placeholder...")
        # Vytvoření placeholder zmrzlin
        placeholders = []
        colors = [(255, 200, 150), (139, 69, 19), (144, 238, 144), (255, 182, 193), (255, 255, 224)]
        
        for color in colors:
            placeholder = pygame.Surface((80, 120), pygame.SRCALPHA)
            # Kornout
            pygame.draw.polygon(placeholder, (210, 180, 140), [(40, 30), (20, 115), (60, 115)])
            # Kopeček
            pygame.draw.circle(placeholder, color, (40, 35), 25)
            placeholders.append(placeholder)
        
        return placeholders

# NOVÉ: Animace plovoucích zmrzlin pro pozadí
class FloatingIcecream:
    def __init__(self, image, x, y):
        self.image = image
        self.original_y = y
        self.x = x
        self.y = y
        self.float_offset = 0
        self.float_speed = random.uniform(0.02, 0.05)
        self.float_amplitude = random.uniform(10, 20)
        self.rotation = 0
        self.rotation_speed = random.uniform(-1, 1)
        self.scale = random.uniform(0.7, 1.3)
        self.alpha = random.randint(100, 200)
        
    def update(self):
        self.float_offset += self.float_speed
        self.y = self.original_y + math.sin(self.float_offset) * self.float_amplitude
        self.rotation += self.rotation_speed
        
    def draw(self, surface):
        # Rotace a průhlednost
        rotated_image = pygame.transform.rotozoom(self.image, self.rotation, self.scale)
        
        # Aplikace průhlednosti
        temp_surface = rotated_image.copy()
        temp_surface.set_alpha(self.alpha)
        
        # Vycentrování rotovaného obrázku
        rect = rotated_image.get_rect(center=(self.x, self.y))
        surface.blit(temp_surface, rect)

# NOVÉ: Gradient pozadí
def draw_gradient_background(surface, color1, color2):
    """Vykreslí vertikální gradient"""
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (WIDTH, y))

# NOVÉ: Vylepšené stylové tlačítko bez stínu
def draw_fancy_button_no_shadow(surface, rect, text, font, hover=False):
    """Vykreslí vylepšené stylové tlačítko bez stínu"""
    # NOVÉ: Animace tlačítka při hover
    if hover:
        # Zvětšení tlačítka při hover
        inflated_rect = rect.copy()
        inflated_rect.inflate_ip(8, 4)  # Mírné zvětšení
        working_rect = inflated_rect
    else:
        working_rect = rect
    
    # ODSTRANĚNO: Všechny stíny
    
    # VYLEPŠENÝ: Složitější gradient pro tlačítko
    if hover:
        # Zlatavé barvy při hover
        color1 = (255, 215, 100)  # Zlatá světlá
        color2 = (255, 180, 50)   # Zlatá střední
        color3 = (220, 140, 30)   # Zlatá tmavá
        border_color = (180, 100, 20)
        text_color = (80, 40, 10)
    else:
        # Oranžové barvy normálně
        color1 = (255, 200, 120)  # Světle oranžová
        color2 = (255, 160, 80)   # Střední oranžová  
        color3 = (220, 120, 50)   # Tmavě oranžová
        border_color = (180, 80, 30)
        text_color = (100, 50, 20)
    
    # NOVÉ: Složitější gradient se třemi barvami
    button_surface = pygame.Surface((working_rect.width, working_rect.height), pygame.SRCALPHA)
    for y in range(working_rect.height):
        if y < working_rect.height // 2:
            # Horní polovina: color1 -> color2
            ratio = y / (working_rect.height // 2)
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        else:
            # Dolní polovina: color2 -> color3
            ratio = (y - working_rect.height // 2) / (working_rect.height // 2)
            r = int(color2[0] * (1 - ratio) + color3[0] * ratio)
            g = int(color2[1] * (1 - ratio) + color3[1] * ratio)
            b = int(color2[2] * (1 - ratio) + color3[2] * ratio)
        pygame.draw.line(button_surface, (r, g, b), (0, y), (working_rect.width, y))
    
    # NOVÉ: Vnější rámeček s gradientem
    pygame.draw.rect(surface, border_color, working_rect, border_radius=18, width=4)
    
    # NOVÉ: Vnitřní světlý rámeček
    inner_border_rect = working_rect.copy()
    inner_border_rect.inflate_ip(-8, -8)
    pygame.draw.rect(surface, (255, 255, 255, 100), inner_border_rect, border_radius=15, width=2)
    
    # Aplikace gradientu
    inner_rect = working_rect.copy()
    inner_rect.inflate_ip(-4, -4)
    
    # Vytvoření masky pro zaoblené rohy
    mask_surface = pygame.Surface((inner_rect.width, inner_rect.height), pygame.SRCALPHA)
    pygame.draw.rect(mask_surface, (255, 255, 255, 255), (0, 0, inner_rect.width, inner_rect.height), border_radius=15)
    
    # Aplikace masky na gradient
    button_surface = pygame.transform.scale(button_surface, (inner_rect.width, inner_rect.height))
    for y in range(inner_rect.height):
        for x in range(inner_rect.width):
            if mask_surface.get_at((x, y))[3] > 0:  # Pokud je pixel v masce viditelný
                surface.set_at((inner_rect.x + x, inner_rect.y + y), button_surface.get_at((x, y)))
    
    # VYLEPŠENÝ: Text s outline efektem
    # Outline (obrys textu)
    outline_positions = [(-2, -2), (-2, 2), (2, -2), (2, 2), (-2, 0), (2, 0), (0, -2), (0, 2)]
    for dx, dy in outline_positions:
        outline_surface = font.render(text, True, (255, 255, 255, 150))
        outline_rect = outline_surface.get_rect(center=(working_rect.centerx + dx, working_rect.centery + dy))
        surface.blit(outline_surface, outline_rect)
    
    # Hlavní text
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=working_rect.center)
    surface.blit(text_surface, text_rect)
    
    # NOVÉ: Světelný efekt nahoře
    highlight_rect = pygame.Rect(working_rect.x + 10, working_rect.y + 8, working_rect.width - 20, 8)
    highlight_surface = pygame.Surface((highlight_rect.width, highlight_rect.height), pygame.SRCALPHA)
    for x in range(highlight_rect.width):
        alpha = int(100 * (1 - abs(x - highlight_rect.width/2) / (highlight_rect.width/2)))
        highlight_surface.set_at((x, 0), (255, 255, 255, alpha))
        highlight_surface.set_at((x, 1), (255, 255, 255, alpha//2))
    surface.blit(highlight_surface, highlight_rect.topleft)
    
    return working_rect

# NOVÉ: Stylový titulek s efekty
def draw_fancy_title(surface, text, font, x, y, shadow_color=(100, 50, 50), main_color=(255, 220, 180)):
    """Vykreslí stylový titulek se stínem"""
    # Stín
    shadow_surface = font.render(text, True, shadow_color)
    surface.blit(shadow_surface, (x + 4, y + 4))
    
    # Hlavní text
    main_surface = font.render(text, True, main_color)
    surface.blit(main_surface, (x, y))

# NOVÉ: Vykreslování pro úvodní obrazovku a menu
def draw_intro_screen(surface):
    """Vykreslí tematickou úvodní obrazovku"""
    # Gradient pozadí (svetle modré k bílé)
    draw_gradient_background(surface, (200, 230, 255), (255, 255, 255))
    
    # Aktualizace a vykreslení plovoucích zmrzlin
    for icecream in floating_icecreams:
        icecream.update()
        icecream.draw(surface)
    
    # Hlavní titulek
    title_font = pygame.font.SysFont("arial", 60, bold=True)
    draw_fancy_title(surface, "Vítejte v Zmrzlinárně!", title_font, 
                    WIDTH // 2 - 300, HEIGHT // 2 - 100)
    
    # Podtitulek
    subtitle_font = pygame.font.SysFont("arial", 24)
    subtitle_text = subtitle_font.render("Připravte se na sladké dobrodružství!", True, (150, 100, 50))
    surface.blit(subtitle_text, (WIDTH // 2 - subtitle_text.get_width() // 2, HEIGHT // 2 - 20))
    
    # UPRAVENO: Dekorativní zmrzliny po stranách (jen 4 zmrzliny místo 5)
    if len(decoration_icecreams) >= 2:
        # Levá strana
        surface.blit(decoration_icecreams[0], (50, HEIGHT // 2 - 60))
        surface.blit(decoration_icecreams[1], (100, HEIGHT // 2 + 20))
        
        # Pravá strana - kontrola existence dalších zmrzlin
        if len(decoration_icecreams) >= 4:
            surface.blit(decoration_icecreams[2], (WIDTH - 130, HEIGHT // 2 - 60))
            surface.blit(decoration_icecreams[3], (WIDTH - 180, HEIGHT // 2 + 20))

def draw_menu_screen(surface, mouse_pos):
    """Vykreslí tematické menu"""
    # Gradient pozadí (růžové k žluté)
    draw_gradient_background(surface, (255, 200, 220), (255, 240, 200))
    
    # ODSTRANĚNO: Animace plovoucích zmrzlin (zůstávají jen na úvodní obrazovce)
    
    # Hlavní titulek menu
    title_font = pygame.font.SysFont("arial", 72, bold=True)
    draw_fancy_title(surface, "ZMRZLINÁRNA", title_font, 
                    WIDTH // 2 - 250, HEIGHT // 2 - 150)
    
    # Stylové tlačítko HRÁT
    button_font = pygame.font.SysFont("arial", 36, bold=True)
    button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 20, 200, 60)  # Posunuto výš
    
    # Kontrola hover efektu
    hover = button_rect.collidepoint(mouse_pos)
    
    button_rect_result = draw_fancy_button_no_shadow(surface, button_rect, "HRÁT", button_font, hover)
    
    # UPRAVENO: Pouze 2 zmrzliny vedle tlačítka HRÁT
    if len(decoration_icecreams) >= 2:
        # Jen po stranách tlačítka
        surface.blit(decoration_icecreams[0], (button_rect.left - 120, button_rect.centery - 60))
        surface.blit(decoration_icecreams[1], (button_rect.right + 40, button_rect.centery - 60))
    
    return button_rect_result

# NOVÉ: Načtení spritesheetů pomocí subsurface()
def load_scoop_spritesheet():
    """Načte spritesheet kopečků a extrahuje jednotlivé kopečky pomocí subsurface()"""
    try:
        spritesheet = pygame.image.load("icecream/assets/Icecream/download.png").convert_alpha()
        
        sheet_width = spritesheet.get_width()
        sheet_height = spritesheet.get_height()
        
        scoop_width = sheet_width // 3
        scoop_height = sheet_height // 3
        
        scoops = {}
        scoop_names = [
            ['raspberry', 'pistachio', 'caramel'],
            ['hazelnut', 'lemon', 'vanilla'], 
            ['peach', 'strawberry', 'chocolate']
        ]
        
        for row in range(3):
            for col in range(3):
                rect = pygame.Rect(col * scoop_width, row * scoop_height, scoop_width, scoop_height)
                scoop_surface = spritesheet.subsurface(rect)
                scoop_name = scoop_names[row][col]
                scoops[scoop_name] = scoop_surface
                
        return scoops
        
    except pygame.error:
        print("Nepodařilo se načíst spritesheet kopečků, používám záložní obrázky...")
        return {
            'chocolate': pygame.image.load("icecream/assets/Icecream/cokoladova.png").convert_alpha(),
            'vanilla': pygame.image.load("icecream/assets/Icecream/smoulova.png").convert_alpha()
        }

def load_cone_spritesheet():
    """NOVÉ: Načte spritesheet kornoutů pomocí subsurface()"""
    try:
        # Načtení spritesheet kornoutů (předpokládám 1x4 nebo 2x2 layout)
        spritesheet = pygame.image.load("icecream/assets/Icecream/cones.png").convert_alpha()
        
        sheet_width = spritesheet.get_width()
        sheet_height = spritesheet.get_height()
        
        # Předpokládám 4 kornouty v řadě (1x4)
        cone_width = sheet_width // 4
        cone_height = sheet_height
        
        cones = {}
        cone_names = ['classic', 'waffle', 'short', 'sugar']
        
        # NOVÉ: Asymetrické oříznutí pro classic kornout s posunutím doleva
        for i in range(4):
            if i == 0:  # Classic kornout - posun doleva pro lepší centrace pod kopeček
                padding_left = int(cone_width * 0.08)   # Méně zleva - posun doleva
                padding_right = int(cone_width * 0.05)  # Mírně více zprava
                padding_y = int(cone_height * 0.06)
                
                rect = pygame.Rect(
                    i * cone_width + padding_left, 
                    padding_y, 
                    cone_width - padding_left - padding_right, 
                    cone_height - 2 * padding_y
                )
            else:  # Ostatní kornouty - symetrické oříznutí
                padding_settings = {
                    1: {'x': int(cone_width * 0.10), 'y': int(cone_height * 0.05)},  # waffle
                    2: {'x': int(cone_width * 0.12), 'y': int(cone_height * 0.06)},  # short  
                    3: {'x': int(cone_width * 0.08), 'y': int(cone_height * 0.05)}   # sugar
                }
                
                padding_x = padding_settings[i]['x']
                padding_y = padding_settings[i]['y']
                
                rect = pygame.Rect(
                    i * cone_width + padding_x, 
                    padding_y, 
                    cone_width - 2 * padding_x, 
                    cone_height - 2 * padding_y
                )
            
            cone_surface = spritesheet.subsurface(rect)
            cone_name = cone_names[i]
            cones[cone_name] = cone_surface
                
        return cones
        
    except pygame.error:
        print("Nepodařilo se načíst spritesheet kornoutů, používám záložní obrázek...")
        # Záložní načtení - vytvoříme více variant ze stejného obrázku
        try:
            cone_img = pygame.image.load("icecream/assets/Icecream/kornout.png").convert_alpha()
            return {
                'classic': cone_img,
                'waffle': cone_img,  # V budoucnu můžete přidat různé kornouty
                'sugar': cone_img,
                'chocolate': cone_img
            }
        except pygame.error:
            print("Nepodařilo se načíst ani záložní kornout!")
            # Vytvoříme jednoduchý placeholder
            placeholder = pygame.Surface((64, 64), pygame.SRCALPHA)
            pygame.draw.polygon(placeholder, (210, 180, 140), [(32, 5), (10, 60), (54, 60)])
            return {'classic': placeholder}

# Načtení obrázků
scoop_images = load_scoop_spritesheet()
cone_images = load_cone_spritesheet()  # NOVÉ: Kornouty ze spritesheet

# NOVÉ: Načtení dekoračních zmrzlin a vytvoření plovoucích animací
decoration_icecreams = load_icecream_decoration()
floating_icecreams = []

# Vytvoření plovoucích zmrzlin pro pozadí
for _ in range(8):
    if decoration_icecreams:
        img = random.choice(decoration_icecreams)
        x = random.randint(50, WIDTH - 50)
        y = random.randint(50, HEIGHT - 50)
        floating_icecreams.append(FloatingIcecream(img, x, y))

# Mapování názvů
flavor_names = {
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

cone_names = {
    'classic': 'klasický',
    'waffle': 'vafle',
    'short': 'malý',
    'sugar': 'cukrový',
}

score = 0
assembly_error = False
error_timer = 0
game_start_time = 0  # NOVÉ: Čas začátku hry
button_rect_global = pygame.Rect(0, 0, 0, 0)  # Globální proměnná pro tlačítko

class DraggableItem:
    def __init__(self, image, label, start_pos, item_key=None, item_type="scoop"):
        self.original_image = image
        self.image = pygame.transform.scale(image, (48, 48))
        self.label = label
        self.item_key = item_key  # klíč pro identifikaci (flavor pro scoop, cone_type pro cone)
        self.item_type = item_type  # "scoop" nebo "cone"
        self.start_pos = start_pos
        self.rect = self.image.get_rect(topleft=start_pos)
        self.dragging = False
        self.offset = (0, 0)
        self.placed = False
        
        # NOVÉ: Animace
        self.hover_scale = 1.0
        self.target_scale = 1.0
        self.bounce_offset = 0
        self.bounce_speed = 0.1

    def update_animation(self):
        """NOVÉ: Aktualizuje animace pro předmět"""
        mouse_pos = pygame.mouse.get_pos()
        
        # Hover efekt - zvětšení při najetí myší
        if self.rect.collidepoint(mouse_pos) and not self.placed:
            self.target_scale = 1.2
        else:
            self.target_scale = 1.0
        
        # Plynulé přechody měřítka
        scale_diff = self.target_scale - self.hover_scale
        self.hover_scale += scale_diff * 0.15
        
        # Bounce animace pro umístěné předměty
        if self.placed:
            self.bounce_offset += self.bounce_speed
            if self.bounce_offset > 6.28:  # 2*π
                self.bounce_offset = 0

    def draw(self, surface):
        # NOVÉ: Aplikace animací při vykreslování
        if self.placed:
            # UPRAVENO: Žádné animace pro umístěné předměty - jen standardní vykreslení
            draw_pos = self.rect.topleft
        else:
            # Hover efekt pro neumístěné předměty
            if abs(self.hover_scale - 1.0) > 0.01:
                scaled_size = int(48 * self.hover_scale)
                scaled_image = pygame.transform.scale(self.original_image, (scaled_size, scaled_size))
                # Vycentrování zvětšeného obrázku
                center_offset = (48 - scaled_size) // 2
                draw_pos = (self.rect.x + center_offset, self.rect.y + center_offset)
                surface.blit(scaled_image, draw_pos)
                return
            else:
                draw_pos = self.rect.topleft
        
        surface.blit(self.image, draw_pos)

    def reset_position(self):
        self.rect.topleft = self.start_pos
        self.placed = False
        self.dragging = False
        self.bounce_offset = 0  # NOVÉ: Reset animace

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos) and not self.placed:
                self.dragging = True
                mouse_x, mouse_y = event.pos
                self.offset = (self.rect.x - mouse_x, self.rect.y - mouse_y)

        elif event.type == pygame.MOUSEBUTTONUP:
            if self.dragging:
                self.dragging = False
                assembly_zone = pygame.Rect(ASSEMBLY_CENTER[0] - 50, ASSEMBLY_CENTER[1] - 150, 100, 200)
                if assembly_zone.colliderect(self.rect):
                    # Kornouty jdou dolů, kopečky nahoru
                    if self.item_type == "cone":
                        self.rect.center = (ASSEMBLY_CENTER[0], ASSEMBLY_CENTER[1] + 20)
                    else:
                        self.rect.center = (ASSEMBLY_CENTER[0], ASSEMBLY_CENTER[1] - len([item for item in assembled_items if item.item_type == "scoop"]) * 25)
                    assembled_items.append(self)
                    self.placed = True
                else:
                    self.reset_position()

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                mouse_x, mouse_y = event.pos
                self.rect.x = mouse_x + self.offset[0]
                self.rect.y = mouse_y + self.offset[1]

class Customer(pygame.sprite.Sprite):
    spacing = 60  # NOVÉ: Zmenšené rozestupy mezi zákazníky (z 80 na 60)
    def __init__(self, customer_id):
        super().__init__()
        image_path = "icecream/assets/Customers/Customer1FF.png"
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()

        self.customer_id = customer_id
        self.order = Order()
        self.show_order = False
        self.font = pygame.font.SysFont("arial", 14)

        self.target_y = 100

        if customer_id == 0:
            self.rect.topleft = (-self.rect.width, self.target_y)
            self.target_x = WIDTH // 2 - 100
        else:
            self.rect.topleft = (-self.rect.width, self.target_y)
            if customer_id == 1:
                self.target_x = WIDTH // 2 - 100 - 3 * self.spacing
            elif customer_id >= 2:
                self.target_x = WIDTH // 2 - 100 - 3 * self.spacing - (customer_id - 1) * self.spacing

        self.speed = 4  # NOVÉ: Zvýšená rychlost pohybu (z 2 na 4)
        self.arrived = False
        self.served = False

    def update(self):
        if not self.arrived:
            if self.rect.centerx < self.target_x:
                self.rect.centerx += self.speed
            if self.rect.centery > self.target_y:
                self.rect.centery -= self.speed
            elif self.rect.centery < self.target_y:
                self.rect.centery += self.speed

            if (abs(self.rect.centerx - self.target_x) < 3 and 
                abs(self.rect.centery - self.target_y) < 3):  # NOVÉ: Zmenšená tolerance pro rychlejší "dorazení" (z 5 na 3)
                self.arrived = True
                if self.customer_id == 0:
                    self.show_order = True

    def move_in_queue(self, new_position):
        self.customer_id = new_position
        self.target_y = 100

        if new_position == 0:
            self.target_x = WIDTH // 2 - 100
        elif new_position == 1:
            self.target_x = WIDTH // 2 - 100 - 200
        else:
            self.target_x = WIDTH // 2 - 100 - 200 - (new_position - 1) * 60

        if (abs(self.rect.centerx - self.target_x) > 3 or 
            abs(self.rect.centery - self.target_y) > 3):  # NOVÉ: Konzistentní tolerance (z 5 na 3)
            self.arrived = False
            self.show_order = False

    def draw_order(self, surface):
        if self.show_order and self.order and not self.served:
            text = self.order.get_text()
            text_surface = order_font.render(text, True, BLACK)
            bubble_x = WIDTH // 2 - 100 - text_surface.get_width() // 2
            bubble_y = 40
            padding = 12
            bubble_rect = pygame.Rect(bubble_x - padding, bubble_y - padding, 
                                      text_surface.get_width() + 2 * padding, 
                                      text_surface.get_height() + 2 * padding)
            pygame.draw.rect(surface, YELLOW, bubble_rect, border_radius=10)
            pygame.draw.rect(surface, BLACK, bubble_rect, 3, border_radius=10)
            title_text = small_font.render("AKTUÁLNÍ OBJEDNÁVKA", True, RED)
            title_x = bubble_x + (bubble_rect.width - title_text.get_width()) // 2
            surface.blit(title_text, (title_x, bubble_y - padding - 25))
            surface.blit(text_surface, (bubble_x, bubble_y))

    def serve(self):
        self.served = True
        self.show_order = False
        self.kill()

class Order:
    def __init__(self):
        # NOVÉ: Výběr kornoutu ze spritesheet
        available_cones = list(cone_names.keys())
        self.cone = random.choice(available_cones)
        
        # Výběr kopečků
        available_flavors = list(flavor_names.keys())
        num_scoops = random.randint(1, 3)
        self.scoops = random.sample(available_flavors, num_scoops)

    def get_text(self):
        czech_cone = cone_names[self.cone]
        czech_flavors = [flavor_names[flavor] for flavor in self.scoops]
        return f"{czech_cone} kornout, {', '.join(czech_flavors)}"

def check_order_correctness():
    if not customer_queue or not assembled_items:
        return False

    current_customer = customer_queue[0]
    recipe = {"cone": None, "scoops": []}
    
    for item in assembled_items:
        if item.item_type == "cone" and item.item_key:
            recipe["cone"] = item.item_key
        elif item.item_type == "scoop" and item.item_key:
            recipe["scoops"].append(item.item_key)

    return (recipe['cone'] == current_customer.order.cone and 
            set(recipe['scoops']) == set(current_customer.order.scoops))

def reset_assembly():
    global assembled_items, assembly_error
    for item in assembled_items:
        item.reset_position()
    assembled_items.clear()
    assembly_error = False

def complete_order():
    global score, assembly_error, error_timer

    if not customer_queue:
        return

    if check_order_correctness():
        score += 1
        served_customer = customer_queue.pop(0)
        served_customer.serve()
        all_sprites.remove(served_customer)
        for i, customer in enumerate(customer_queue):
            customer.move_in_queue(i)
        reset_assembly()
        assembly_error = False
    else:
        assembly_error = True
        error_timer = pygame.time.get_ticks()

def add_new_customer():
    global next_customer_id
    if len(customer_queue) >= 4:
        return
    new_customer = Customer(len(customer_queue))
    customer_queue.append(new_customer)
    all_sprites.add(new_customer)
    next_customer_id += 1
    next_customer_delay = random.randint(3000, 5000)  # NOVÉ: Kratší intervaly mezi zákazníky (z 5000-8000 na 3000-5000)
    pygame.time.set_timer(pygame.USEREVENT + 2, next_customer_delay)

def create_buttons():
    button_width, button_height = 100, 30
    button_y = ASSEMBLY_CENTER[1] + 80
    
    done_button = pygame.Rect(ASSEMBLY_CENTER[0] - button_width - 10, button_y, button_width, button_height)
    reset_button = pygame.Rect(ASSEMBLY_CENTER[0] + 10, button_y, button_width, button_height)
    
    return done_button, reset_button

def draw_buttons(surface, done_button, reset_button):
    color = LIGHT_GREEN if assembled_items else LIGHT_GRAY
    pygame.draw.rect(surface, color, done_button, border_radius=5)
    pygame.draw.rect(surface, BLACK, done_button, 2, border_radius=5)
    
    done_text = button_font.render("HOTOVO", True, BLACK)
    text_rect = done_text.get_rect(center=done_button.center)
    surface.blit(done_text, text_rect)
    
    pygame.draw.rect(surface, LIGHT_RED, reset_button, border_radius=5)
    pygame.draw.rect(surface, BLACK, reset_button, 2, border_radius=5)
    
    reset_text = button_font.render("ZNOVU", True, BLACK)
    text_rect = reset_text.get_rect(center=reset_button.center)
    surface.blit(reset_text, text_rect)

# NOVÉ: Vylepšené rozhraní pro ingredience
def draw_ingredient_panels(surface, drag_items):
    # Panel pro kornouty - VĚTŠÍ PRO 4 KORNOUTY
    cone_panel_rect = pygame.Rect(WIDTH - 300, 20, 135, 280)
    pygame.draw.rect(surface, PANEL_COLOR, cone_panel_rect, border_radius=8)
    pygame.draw.rect(surface, BLACK, cone_panel_rect, 2, border_radius=8)
    
    cone_title = section_font.render("KORNOUTY", True, (100, 50, 150))
    surface.blit(cone_title, (cone_panel_rect.x + 10, cone_panel_rect.y + 10))
    
    # Panel pro kopečky - VĚTŠÍ PRO 9 KOPEČKŮ
    scoop_panel_rect = pygame.Rect(WIDTH - 160, 20, 135, 500)
    pygame.draw.rect(surface, PANEL_COLOR, scoop_panel_rect, border_radius=8)
    pygame.draw.rect(surface, BLACK, scoop_panel_rect, 2, border_radius=8)
    
    scoop_title = section_font.render("KOPEČKY", True, (150, 100, 50))
    surface.blit(scoop_title, (scoop_panel_rect.x + 10, scoop_panel_rect.y + 10))
    
    # NOVÉ: Aktualizace a vykreslení ingrediencí s animacemi
    for item in drag_items:
        if not item.placed:
            item.update_animation()  # Aktualizace animací
            item.draw(surface)
    
    # UPRAVENO: Popisky se vykreslují POTÉ, co se vykreslí všechny ingredience
    # Díky tomu se při drag & drop nepřesouvají názvy s obrázky
    for item in drag_items:
        if not item.placed and not item.dragging:  # Popisky jen pro ne-tažené ingredience
            # Popisky
            if item.item_type == "cone" and item.item_key:
                cone_text = small_font.render(cone_names[item.item_key], True, BLACK)
                surface.blit(cone_text, (item.rect.right + 5, item.rect.centery - 8))
            elif item.item_type == "scoop" and item.item_key:
                flavor_text = small_font.render(flavor_names[item.item_key], True, BLACK)
                surface.blit(flavor_text, (item.rect.right + 5, item.rect.centery - 8))

# NOVÉ: Funkce pro návrat do menu
def return_to_menu():
    global STATE, drag_items, assembled_items, customer_queue, score, assembly_error, all_sprites, game_start_time
    STATE = "menu"
    drag_items.clear()
    assembled_items.clear()
    customer_queue.clear()
    all_sprites.empty()
    score = 0
    assembly_error = False
    game_start_time = 0
    # Zrušení časovače pro nové zákazníky
    pygame.time.set_timer(pygame.USEREVENT + 2, 0)

# NOVÉ: Funkce pro inicializaci hry
def initialize_game():
    global drag_items, game_start_time, score, assembly_error
    drag_items.clear()
    game_start_time = pygame.time.get_ticks()  # Zaznamenání času začátku hry
    score = 0  # NOVÉ: Vynulování skóre při každé nové hře
    assembly_error = False  # Reset chybového stavu
    
    # Kornouty ze spritesheet - VŠECHNY 4 TYPY
    cone_types = ['classic', 'waffle', 'short', 'sugar']
    for i, cone_type in enumerate(cone_types):
        if cone_type in cone_images:
            y_pos = 50 + (i * 60)
            cone_item = DraggableItem(
                cone_images[cone_type], 
                f"cone_{cone_type}", 
                (WIDTH - 290, y_pos),
                item_key=cone_type,
                item_type="cone"
            )
            drag_items.append(cone_item)
    
    # Kopečky ze spritesheet - VŠECH 9 PŘÍCHUTÍ
    flavors_to_show = ['raspberry', 'pistachio', 'caramel', 'hazelnut', 'lemon', 'vanilla', 'peach', 'strawberry', 'chocolate']
    for i, flavor in enumerate(flavors_to_show):
        if flavor in scoop_images:
            y_pos = 50 + (i * 50)
            scoop_item = DraggableItem(
                scoop_images[flavor], 
                f"scoop_{flavor}", 
                (WIDTH - 150, y_pos),
                item_key=flavor,
                item_type="scoop"
            )
            drag_items.append(scoop_item)

# NOVÉ: Funkce pro výpočet zbývajícího času
def get_time_left():
    if game_start_time == 0:
        return 60
    elapsed = (pygame.time.get_ticks() - game_start_time) // 1000
    return max(0, 60 - elapsed)

# NOVÉ: Funkce pro zobrazení nápovědy ovládání
def draw_controls_help(surface, state):
    help_texts = []
    
    if state == "menu":
        help_texts = [
            "OVLÁDÁNÍ:",
            "Enter - Spustit hru",
            "Escape - Ukončit hru"
        ]
    elif state == "playing":
        help_texts = [
            "OVLÁDÁNÍ:",
            "Enter - Dokončit objednávku",
            "Mezerník - Reset sestavování",
            "Escape - Návrat do menu"
        ]
    
    # Posun do levého spodního rohu
    y_start = HEIGHT - (len(help_texts) * 20) - 10
    for i, text in enumerate(help_texts):
        if i == 0:  # UPRAVENO: Nadpis "OVLÁDÁNÍ" černě a tučně
            help_surface = section_font.render(text, True, BLACK)  # Tučný font
        else:
            help_surface = small_font.render(text, True, BLACK)
        surface.blit(help_surface, (10, y_start + i * 20))

# NOVÉ: Funkce pro graficky zajímavé skóre
def draw_score(surface, score):
    # Pozadí pro skóre
    score_bg_rect = pygame.Rect(15, ASSEMBLY_CENTER[1] - 50, 200, 60)
    pygame.draw.rect(surface, (50, 50, 100), score_bg_rect, border_radius=10)
    pygame.draw.rect(surface, (100, 150, 255), score_bg_rect, 3, border_radius=10)
    
    # Gradient efekt (simulace pomocí více obdélníků)
    for i in range(5):
        alpha = 50 - i * 10
        gradient_rect = pygame.Rect(score_bg_rect.x + i, score_bg_rect.y + i, 
                                   score_bg_rect.width - 2*i, score_bg_rect.height - 2*i)
        gradient_surface = pygame.Surface((gradient_rect.width, gradient_rect.height), pygame.SRCALPHA)
        gradient_surface.fill((100, 150, 255, alpha))
        surface.blit(gradient_surface, gradient_rect.topleft)
    
    # Titulek "SKÓRE"
    score_title = small_font.render("SKÓRE", True, (200, 220, 255))
    title_x = score_bg_rect.x + (score_bg_rect.width - score_title.get_width()) // 2
    surface.blit(score_title, (title_x, score_bg_rect.y + 8))
    
    # Hlavní číslo skóre - větší font
    score_font = pygame.font.SysFont("arial", 28, bold=True)
    score_text = score_font.render(str(score), True, (255, 255, 100))
    score_x = score_bg_rect.x + (score_bg_rect.width - score_text.get_width()) // 2
    surface.blit(score_text, (score_x, score_bg_rect.y + 28))

# NOVÉ: Funkce pro zobrazení časomíry
def draw_timer(surface, time_left):
    # Pozadí pro časomíru
    timer_bg_rect = pygame.Rect(15, ASSEMBLY_CENTER[1] - 130, 200, 60)
    
    # Barva pozadí se mění podle zbývajícího času
    if time_left > 30:
        bg_color = (50, 100, 50)  # Zelená
        border_color = (100, 255, 100)
    elif time_left > 15:
        bg_color = (100, 100, 50)  # Žlutá
        border_color = (255, 255, 100)
    else:
        bg_color = (100, 50, 50)  # Červená
        border_color = (255, 100, 100)
    
    pygame.draw.rect(surface, bg_color, timer_bg_rect, border_radius=10)
    pygame.draw.rect(surface, border_color, timer_bg_rect, 3, border_radius=10)
    
    # Gradient efekt
    for i in range(5):
        alpha = 50 - i * 10
        gradient_rect = pygame.Rect(timer_bg_rect.x + i, timer_bg_rect.y + i, 
                                   timer_bg_rect.width - 2*i, timer_bg_rect.height - 2*i)
        gradient_surface = pygame.Surface((gradient_rect.width, gradient_rect.height), pygame.SRCALPHA)
        gradient_surface.fill((*border_color, alpha))
        surface.blit(gradient_surface, gradient_rect.topleft)
    
    # Titulek "ČAS"
    timer_title = small_font.render("ČAS", True, (200, 220, 255))
    title_x = timer_bg_rect.x + (timer_bg_rect.width - timer_title.get_width()) // 2
    surface.blit(timer_title, (title_x, timer_bg_rect.y + 8))
    
    # Zbývající čas - větší font
    timer_font = pygame.font.SysFont("arial", 28, bold=True)
    timer_text = timer_font.render(f"{time_left}s", True, (255, 255, 255))
    timer_x = timer_bg_rect.x + (timer_bg_rect.width - timer_text.get_width()) // 2
    surface.blit(timer_text, (timer_x, timer_bg_rect.y + 28))

# NOVÉ: Funkce pro zobrazení finálního skóre
def draw_final_score(surface, final_score):
    # Pozadí pro finální skóre
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))  # Průhledné černé pozadí
    surface.blit(overlay, (0, 0))
    
    # Hlavní panel s finálním skóre
    panel_width, panel_height = 400, 300
    panel_rect = pygame.Rect((WIDTH - panel_width) // 2, (HEIGHT - panel_height) // 2, panel_width, panel_height)
    pygame.draw.rect(surface, (30, 30, 60), panel_rect, border_radius=15)
    pygame.draw.rect(surface, (100, 150, 255), panel_rect, 5, border_radius=15)
    
    # Gradient efekt pro panel
    for i in range(8):
        alpha = 60 - i * 7
        gradient_rect = pygame.Rect(panel_rect.x + i, panel_rect.y + i, 
                                   panel_rect.width - 2*i, panel_rect.height - 2*i)
        gradient_surface = pygame.Surface((gradient_rect.width, gradient_rect.height), pygame.SRCALPHA)
        gradient_surface.fill((100, 150, 255, alpha))
        surface.blit(gradient_surface, gradient_rect.topleft)
    
    # Texty
    title_font = pygame.font.SysFont("arial", 36, bold=True)
    score_font = pygame.font.SysFont("arial", 48, bold=True)
    instruction_font = pygame.font.SysFont("arial", 20)
    
    # "ČAS VYPRŠEL!"
    title_text = title_font.render("ČAS VYPRŠEL!", True, (255, 100, 100))
    title_x = panel_rect.x + (panel_rect.width - title_text.get_width()) // 2
    surface.blit(title_text, (title_x, panel_rect.y + 40))
    
    # "FINÁLNÍ SKÓRE"
    final_title = instruction_font.render("FINÁLNÍ SKÓRE:", True, (200, 220, 255))
    final_title_x = panel_rect.x + (panel_rect.width - final_title.get_width()) // 2
    surface.blit(final_title, (final_title_x, panel_rect.y + 100))
    
    # Samotné skóre - velké číslo
    score_text = score_font.render(str(final_score), True, (255, 255, 100))
    score_x = panel_rect.x + (panel_rect.width - score_text.get_width()) // 2
    surface.blit(score_text, (score_x, panel_rect.y + 130))
    
    # Instrukce
    instruction1 = instruction_font.render("Stiskněte Enter pro novou hru", True, (200, 220, 255))
    instruction1_x = panel_rect.x + (panel_rect.width - instruction1.get_width()) // 2
    surface.blit(instruction1, (instruction1_x, panel_rect.y + 210))
    
    instruction2 = instruction_font.render("nebo Escape pro návrat do menu", True, (200, 220, 255))
    instruction2_x = panel_rect.x + (panel_rect.width - instruction2.get_width()) // 2
    surface.blit(instruction2, (instruction2_x, panel_rect.y + 235))

STATE = "intro"
drag_items = []
assembled_items = []
customer_queue = []
next_customer_id = 0
all_sprites = pygame.sprite.Group()
intro_start_time = pygame.time.get_ticks()

done_button, reset_button = create_buttons()

# --- Hlavní smyčka ---
running = True
while running:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.USEREVENT + 2:
            add_new_customer()
        
        # NOVÉ: Ovládání klávesnicí
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if STATE == "playing" or STATE == "game_over":
                    return_to_menu()
                elif STATE == "menu":
                    running = False
            elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                if STATE == "menu" or STATE == "game_over":
                    initialize_game()
                    STATE = "playing"
                    add_new_customer()
                elif STATE == "playing" and assembled_items:
                    complete_order()
            elif event.key == pygame.K_SPACE:
                if STATE == "playing":
                    reset_assembly()
                    
        elif STATE == "menu":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect_global.collidepoint(event.pos):
                    initialize_game()
                    STATE = "playing"
                    add_new_customer()
                    
        elif STATE == "playing":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if done_button.collidepoint(event.pos) and assembled_items:
                    complete_order()
                elif reset_button.collidepoint(event.pos):
                    reset_assembly()
            
            for item in drag_items:
                item.handle_event(event)

    # Vykreslování
    screen.fill(WHITE)
    
    if STATE == "intro":
        draw_intro_screen(screen)
        # UPRAVENO: Prodloužen čas zobrazení úvodní obrazovky ze 3 na 4 sekundy
        if pygame.time.get_ticks() - intro_start_time > 4000:
            STATE = "menu"

    elif STATE == "menu":
        mouse_pos = pygame.mouse.get_pos()
        button_rect_global = draw_menu_screen(screen, mouse_pos)
        
        # Zobrazení nápovědy ovládání
        draw_controls_help(screen, "menu")

    elif STATE == "playing":
        # NOVÉ: Kontrola časomíry
        time_left = get_time_left()
        if time_left <= 0:
            STATE = "game_over"
            # Zrušení časovače pro nové zákazníky
            pygame.time.set_timer(pygame.USEREVENT + 2, 0)
        
        all_sprites.update()
        all_sprites.draw(screen)

        # Vykreslení oblasti pro sestavování
        assembly_zone = pygame.Rect(ASSEMBLY_CENTER[0] - 50, ASSEMBLY_CENTER[1] - 150, 100, 200)
        
        # UPRAVENO: Design stejný jako u panelů ingrediencí
        if assembly_error:
            if pygame.time.get_ticks() - error_timer < 3000:
                if (pygame.time.get_ticks() - error_timer) // 300 % 2 == 0:
                    assembly_color = ASSEMBLY_ERROR
                    border_color = RED
                else:
                    assembly_color = PANEL_COLOR  # Stejná barva jako panely
                    border_color = BLACK  # Černý rámeček
            else:
                assembly_error = False
                assembly_color = PANEL_COLOR  # Stejná barva jako panely
                border_color = BLACK  # Černý rámeček
        else:
            assembly_color = PANEL_COLOR  # Stejná barva jako panely
            border_color = BLACK  # Černý rámeček
        
        pygame.draw.rect(screen, assembly_color, assembly_zone, border_radius=8)  # Stejné border_radius jako panely
        pygame.draw.rect(screen, border_color, assembly_zone, 2, border_radius=8)  # Stejná tloušťka jako panely
        
        if assembly_error and pygame.time.get_ticks() - error_timer < 3000:
            assembly_title = small_font.render("CHYBNÁ OBJEDNÁVKA!", True, RED)
        else:
            # UPRAVENO: Nový text a černá barva
            assembly_title = small_font.render("SESTAV OBJEDNÁVKU", True, BLACK)
        screen.blit(assembly_title, (assembly_zone.centerx - assembly_title.get_width() // 2, assembly_zone.top - 25))

        for item in assembled_items:
            # UPRAVENO: Žádné animace pro umístěné předměty
            item.draw(screen)

        # NOVÉ: Vykreslení rozdělených panelů
        draw_ingredient_panels(screen, drag_items)

        draw_buttons(screen, done_button, reset_button)

        # NOVÉ: Graficky zajímavé skóre a časomíra
        draw_score(screen, score)
        draw_timer(screen, time_left)

        for customer in customer_queue:
            customer.draw_order(screen)

        if customer_queue:
            queue_text = small_font.render(f"Zákazníků ve frontě: {len(customer_queue)}", True, BLACK)
            screen.blit(queue_text, (20, 70))
        
        # NOVÉ: Zobrazení nápovědy ovládání
        draw_controls_help(screen, "playing")
    
    elif STATE == "game_over":
        # NOVÉ: Obrazovka s finálním skóre
        draw_final_score(screen, score)

    pygame.display.flip()

pygame.quit()
sys.exit()