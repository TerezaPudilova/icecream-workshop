import pygame
import sys
import random

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
        
        for i in range(4):
            rect = pygame.Rect(i * cone_width, 0, cone_width, cone_height)
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

# NOVÉ: Načtení pozadí pro menu a úvodní obrazovku
def load_background_image():
    """Načte obrázek pozadí pro menu a úvodní obrazovku"""
    try:
        # Pokusíme se načíst obrázek zmrzliny
        background = pygame.image.load("icecream/assets/Icecream/zmrzlina_pozadi.jpg").convert()
        # Změníme velikost na velikost okna
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
        return background
    except pygame.error:
        print("Nepodařilo se načíst pozadí, používám jednobarevné pozadí...")
        # Vytvoříme gradient pozadí jako náhradu
        background = pygame.Surface((WIDTH, HEIGHT))
        for y in range(HEIGHT):
            # Gradient od růžové k oranžové
            color_ratio = y / HEIGHT
            r = int(255 * (0.9 + 0.1 * color_ratio))
            g = int(180 * (0.8 + 0.2 * color_ratio))
            b = int(150 * (0.7 + 0.3 * color_ratio))
            pygame.draw.line(background, (r, g, b), (0, y), (WIDTH, y))
        return background

background_image = load_background_image()

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
        color = (100, 100, 100) if i == 0 else BLACK
        help_surface = small_font.render(text, True, color)
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
                if button_rect.collidepoint(event.pos):
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
        # NOVÉ: Pozadí pro úvodní obrazovku
        screen.blit(background_image, (0, 0))
        
        # Poloprůhledné pozadí pro text
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))  # Černé s průhledností
        screen.blit(overlay, (0, 0))
        
        text = font.render("Vítejte v Zmrzlinárně!", True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        
        # Stín pro text
        shadow_text = font.render("Vítejte v Zmrzlinárně!", True, BLACK)
        shadow_rect = shadow_text.get_rect(center=(WIDTH // 2 + 3, HEIGHT // 2 - 47))
        screen.blit(shadow_text, shadow_rect)
        screen.blit(text, text_rect)
        
        if pygame.time.get_ticks() - intro_start_time > 3000:
            STATE = "menu"

    elif STATE == "menu":
        # NOVÉ: Pozadí pro menu
        screen.blit(background_image, (0, 0))
        
        # Poloprůhledné pozadí pro UI
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100))  # Černé s průhledností
        screen.blit(overlay, (0, 0))
        
        # Titulek menu
        title_text = font.render("MENU", True, WHITE)
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
        
        # Stín pro titulek
        title_shadow = font.render("MENU", True, BLACK)
        title_shadow_rect = title_shadow.get_rect(center=(WIDTH // 2 + 3, HEIGHT // 2 - 97))
        screen.blit(title_shadow, title_shadow_rect)
        screen.blit(title_text, title_rect)
        
        # Tlačítko hrát
        button_text = font.render("HRÁT", True, WHITE)
        button_rect = button_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        
        # Pozadí tlačítka
        button_bg_rect = pygame.Rect(button_rect.x - 20, button_rect.y - 10, 
                                    button_rect.width + 40, button_rect.height + 20)
        pygame.draw.rect(screen, (100, 50, 150, 180), button_bg_rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, button_bg_rect, 3, border_radius=10)
        
        # Stín pro tlačítko
        button_shadow = font.render("HRÁT", True, BLACK)
        button_shadow_rect = button_shadow.get_rect(center=(WIDTH // 2 + 2, HEIGHT // 2 + 2))
        screen.blit(button_shadow, button_shadow_rect)
        screen.blit(button_text, button_rect)
        
        # NOVÉ: Zobrazení nápovědy ovládání
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
        
        if assembly_error:
            if pygame.time.get_ticks() - error_timer < 3000:
                if (pygame.time.get_ticks() - error_timer) // 300 % 2 == 0:
                    assembly_color = ASSEMBLY_ERROR
                    border_color = RED
                else:
                    assembly_color = ASSEMBLY_NORMAL
                    border_color = (100, 100, 200)
            else:
                assembly_error = False
                assembly_color = ASSEMBLY_NORMAL
                border_color = (100, 100, 200)
        else:
            assembly_color = ASSEMBLY_NORMAL
            border_color = (100, 100, 200)
        
        pygame.draw.rect(screen, assembly_color, assembly_zone, border_radius=10)
        pygame.draw.rect(screen, border_color, assembly_zone, 3, border_radius=10)
        
        if assembly_error and pygame.time.get_ticks() - error_timer < 3000:
            assembly_title = small_font.render("CHYBNÁ OBJEDNÁVKA!", True, RED)
        else:
            assembly_title = small_font.render("MÍSTO PRO SESTAVOVÁNÍ", True, (50, 50, 150))
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