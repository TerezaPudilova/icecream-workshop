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

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    def reset_position(self):
        self.rect.topleft = self.start_pos
        self.placed = False
        self.dragging = False

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
    spacing = 80
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

        self.speed = 2
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

            if (abs(self.rect.centerx - self.target_x) < 5 and 
                abs(self.rect.centery - self.target_y) < 5):
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

        if (abs(self.rect.centerx - self.target_x) > 5 or 
            abs(self.rect.centery - self.target_y) > 5):
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
    next_customer_delay = random.randint(5000, 8000)
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
    
    # Vykreslení ingrediencí
    for item in drag_items:
        if not item.placed:
            item.draw(surface)
            
            # Popisky
            if item.item_type == "cone" and item.item_key:
                cone_text = small_font.render(cone_names[item.item_key], True, BLACK)
                surface.blit(cone_text, (item.rect.right + 5, item.rect.centery - 8))
            elif item.item_type == "scoop" and item.item_key:
                flavor_text = small_font.render(flavor_names[item.item_key], True, BLACK)
                surface.blit(flavor_text, (item.rect.right + 5, item.rect.centery - 8))

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
            
        elif STATE == "menu":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    # NOVÉ: Inicializace ingrediencí s rozdělenými panely
                    drag_items.clear()
                    
                    # Kornouty ze spritesheet - VŠECHNY 4 TYPY
                    cone_types = ['classic', 'waffle', 'short', 'sugar']  # Všechny 4 kornouty
                    for i, cone_type in enumerate(cone_types):
                        if cone_type in cone_images:
                            y_pos = 50 + (i * 60)  # Menší rozestup pro 4 kornouty
                            cone_item = DraggableItem(
                                cone_images[cone_type], 
                                f"cone_{cone_type}", 
                                (WIDTH - 290, y_pos),
                                item_key=cone_type,
                                item_type="cone"
                            )
                            drag_items.append(cone_item)
                    
                    # Kopečky ze spritesheet - VŠECH 9 PŘÍCHUTÍ
                    flavors_to_show = ['raspberry', 'pistachio', 'caramel', 'hazelnut', 'lemon', 'vanilla', 'peach', 'strawberry', 'chocolate']  # Všech 9 příchutí
                    for i, flavor in enumerate(flavors_to_show):
                        if flavor in scoop_images:
                            y_pos = 50 + (i * 50)  # Menší rozestup pro 9 kopečků
                            scoop_item = DraggableItem(
                                scoop_images[flavor], 
                                f"scoop_{flavor}", 
                                (WIDTH - 150, y_pos),
                                item_key=flavor,
                                item_type="scoop"
                            )
                            drag_items.append(scoop_item)
                    
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
        text = font.render("Vítejte v Zmrzlinárně!", True, BLACK)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 50))
        if pygame.time.get_ticks() - intro_start_time > 3000:
            STATE = "menu"

    elif STATE == "menu":
        text = font.render("MENU", True, BLACK)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 100))
        button_text = font.render("HRÁT", True, BLACK)
        button_rect = button_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(button_text, button_rect)

    elif STATE == "playing":
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
            item.draw(screen)

        # NOVÉ: Vykreslení rozdělených panelů
        draw_ingredient_panels(screen, drag_items)

        draw_buttons(screen, done_button, reset_button)

        score_text = small_font.render(f"Skóre: {score}", True, BLACK)
        screen.blit(score_text, (20, ASSEMBLY_CENTER[1] - 20))

        for customer in customer_queue:
            customer.draw_order(screen)

        if customer_queue:
            queue_text = small_font.render(f"Zákazníků ve frontě: {len(customer_queue)}", True, BLACK)
            screen.blit(queue_text, (20, 70))

    pygame.display.flip()

pygame.quit()
sys.exit()