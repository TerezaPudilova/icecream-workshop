import pygame
import sys
import random

# Inicializace Pygame
pygame.init()

# Nastavení velikosti okna
WIDTH, HEIGHT = 1000, 600  # Zvětšeno kvůli objednávkám
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Obsluha Zmrzlinárny")

ASSEMBLY_CENTER = (WIDTH // 2, HEIGHT // 2 + 100)

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
ASSEMBLY_NORMAL = (240, 240, 255)
ASSEMBLY_ERROR = (255, 200, 200)
YELLOW = (255, 255, 0)

# Fonty
font = pygame.font.SysFont("arial", 48)
small_font = pygame.font.SysFont("arial", 16)
button_font = pygame.font.SysFont("arial", 20)
order_font = pygame.font.SysFont("arial", 18)

# Načtení obrázků
cone_img = pygame.image.load("icecream/assets/Icecream/kornout.png").convert_alpha()
scoop1_img = pygame.image.load("icecream/assets/Icecream/cokoladova.png").convert_alpha()
scoop2_img = pygame.image.load("icecream/assets/Icecream/smoulova.png").convert_alpha()

score = 0
assembly_error = False
error_timer = 0

class DraggableItem:
    def __init__(self, image, label, start_pos):
        self.original_image = image
        self.image = pygame.transform.scale(image, (48, 48))
        self.label = label
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
                    self.rect.center = (ASSEMBLY_CENTER[0], ASSEMBLY_CENTER[1] - len(assembled_items) * 30)
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
    spacing = 80  # Rozestup mezi zákazníky ve frontě
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
            self.target_x = WIDTH // 2  # Obsluha uprostřed
        else:
            self.rect.topleft = (-self.rect.width, self.target_y)
            if customer_id == 1:
                self.target_x = WIDTH // 2 - 3 * self.spacing  # Druhý zákazník má trojnásobný rozestup
            elif customer_id >= 2:
                self.target_x = WIDTH // 2 - 3 * self.spacing - (customer_id - 1) * self.spacing  # Další zákazníci se řadí od druhého vlevo

        
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
                if self.customer_id == 0:
                    self.show_order = True

    def move_in_queue(self, new_position):
        self.customer_id = new_position
        self.target_y = 100

        if new_position == 0:
            self.target_x = WIDTH // 2
        elif new_position == 1:
            self.target_x = WIDTH // 2 - 200
        else:
            self.target_x = WIDTH // 2 - 200 - (new_position - 1) * 60

        if (abs(self.rect.centerx - self.target_x) > 5 or 
            abs(self.rect.centery - self.target_y) > 5):
            self.arrived = False
            self.show_order = False


    def draw_order(self, surface):
        if self.show_order and self.order and not self.served:
            text = self.order.get_text()
            text_surface = order_font.render(text, True, BLACK)
            bubble_x = WIDTH // 2 - text_surface.get_width() // 2
            bubble_y = 40
            padding = 12
            bubble_rect = pygame.Rect(bubble_x - padding, bubble_y - padding, 
                                      text_surface.get_width() + 2 * padding, 
                                      text_surface.get_height() + 2 * padding)
            pygame.draw.rect(surface, YELLOW, bubble_rect, border_radius=10)
            pygame.draw.rect(surface, BLACK, bubble_rect, 3, border_radius=10)
            title_text = small_font.render("AKTUÁLNÍ OBJEDNÁVKA", True, RED)
            title_x = WIDTH // 2 - title_text.get_width() // 2
            surface.blit(title_text, (title_x, bubble_y - padding - 25))
            surface.blit(text_surface, (bubble_x, bubble_y))

    def serve(self):
        self.served = True
        self.show_order = False
        self.kill()  # Zmizí z obrazovky po obsloužení
class Order:
    def __init__(self):
        self.cone = "klasický"
        self.scoops = random.sample(["čokoláda", "šmoulová"], random.randint(1, 2))

    def get_text(self):
        return f"{self.cone} kornout, {', '.join(self.scoops)}"
    

def check_order_correctness():
    if not customer_queue or not assembled_items:
        return False

    current_customer = customer_queue[0]
    recipe = {"cone": None, "scoops": []}
    for item in assembled_items:
        if item.label == "cone":
            recipe["cone"] = "klasický"
        elif item.label == "scoop1":
            recipe["scoops"].append("čokoláda")
        elif item.label == "scoop2":
            recipe["scoops"].append("šmoulová")

    return (recipe['cone'] == current_customer.order.cone and 
            recipe['scoops'] == current_customer.order.scoops)

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

# Tlačítka
def create_buttons():
    button_width, button_height = 100, 30
    button_y = ASSEMBLY_CENTER[1] + 80
    
    done_button = pygame.Rect(ASSEMBLY_CENTER[0] - button_width - 10, button_y, button_width, button_height)
    reset_button = pygame.Rect(ASSEMBLY_CENTER[0] + 10, button_y, button_width, button_height)
    
    return done_button, reset_button

def draw_buttons(surface, done_button, reset_button):
    # Tlačítko "Hotovo"
    color = LIGHT_GREEN if assembled_items else LIGHT_GRAY
    pygame.draw.rect(surface, color, done_button, border_radius=5)
    pygame.draw.rect(surface, BLACK, done_button, 2, border_radius=5)
    
    done_text = button_font.render("HOTOVO", True, BLACK)
    text_rect = done_text.get_rect(center=done_button.center)
    surface.blit(done_text, text_rect)
    
    # Tlačítko "Začít znovu"
    pygame.draw.rect(surface, LIGHT_RED, reset_button, border_radius=5)
    pygame.draw.rect(surface, BLACK, reset_button, 2, border_radius=5)
    
    reset_text = button_font.render("ZNOVU", True, BLACK)
    text_rect = reset_text.get_rect(center=reset_button.center)
    surface.blit(reset_text, text_rect)

STATE = "intro"
drag_items = []
assembled_items = []
customer_queue = []
next_customer_id = 0
all_sprites = pygame.sprite.Group()
intro_start_time = pygame.time.get_ticks()

# Vytvoření tlačítek
done_button, reset_button = create_buttons()

# --- Hlavní smyčka ---
running = True
while running:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.USEREVENT + 2:
            # Přidání nového zákazníka
            add_new_customer()
            
        elif STATE == "menu":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    # Inicializace ingrediencí
                    drag_items.clear()
                    cone_item = DraggableItem(cone_img, "cone", (WIDTH - 160 + 10, 60))
                    scoop1_item = DraggableItem(scoop1_img, "scoop1", (WIDTH - 160 + 10, 120))
                    scoop2_item = DraggableItem(scoop2_img, "scoop2", (WIDTH - 160 + 10, 180))
                    drag_items.extend([cone_item, scoop1_item, scoop2_item])
                    STATE = "playing"
                    # Přidání prvního zákazníka a spuštění časovače pro další
                    add_new_customer()
                    
        elif STATE == "playing":
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Kontrola kliknutí na tlačítka
                if done_button.collidepoint(event.pos) and assembled_items:
                    complete_order()
                elif reset_button.collidepoint(event.pos):
                    reset_assembly()
            
            # Zpracování tažení ingrediencí
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
        # Aktualizace a vykreslení spritů
        all_sprites.update()
        all_sprites.draw(screen)

        # Vykreslení oblasti pro sestavování zmrzliny
        assembly_zone = pygame.Rect(ASSEMBLY_CENTER[0] - 50, ASSEMBLY_CENTER[1] - 150, 100, 200)
        
        # Změna barvy podle stavu chyby
        if assembly_error:
            # Kontrola, zda má chyba ještě blikat (3 sekundy)
            if pygame.time.get_ticks() - error_timer < 3000:
                # Blikání každých 300ms
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
        
        # Název oblasti
        if assembly_error and pygame.time.get_ticks() - error_timer < 3000:
            assembly_title = small_font.render("CHYBNÁ OBJEDNÁVKA!", True, RED)
        else:
            assembly_title = small_font.render("MÍSTO PRO SESTAVOVÁNÍ", True, (50, 50, 150))
        screen.blit(assembly_title, (assembly_zone.centerx - assembly_title.get_width() // 2, assembly_zone.top - 25))

        # Vykreslení sestavených ingrediencí
        for item in assembled_items:
            item.draw(screen)

        # Vykreslení panelu ingrediencí
        panel_rect = pygame.Rect(WIDTH - 180, 20, 160, 200)
        pygame.draw.rect(screen, LIGHT_GRAY, panel_rect)
        pygame.draw.rect(screen, BLACK, panel_rect, 2)
        title = small_font.render("Ingredience", True, BLACK)
        screen.blit(title, (panel_rect.x + 10, panel_rect.y + 10))

        # Vykreslení dostupných ingrediencí
        for item in drag_items:
            if not item.placed:
                item.draw(screen)

        # Vykreslení tlačítek
        draw_buttons(screen, done_button, reset_button)

        # Vykreslení skóre
        score_text = small_font.render(f"Skóre: {score}", True, BLACK)
        screen.blit(score_text, (20, ASSEMBLY_CENTER[1] - 20))

        
        # Vykreslení objednávek zákazníků
        for customer in customer_queue:
            customer.draw_order(screen)

        # Informace o frontě
        if customer_queue:
            queue_text = small_font.render(f"Zákazníků ve frontě: {len(customer_queue)}", True, BLACK)
            screen.blit(queue_text, (20, 70))
            
            # Informace o čekající frontě (bez aktuálního zákazníka)
            # waiting_customers = len(customer_queue) - 1
            # if waiting_customers > 0:
            #     waiting_text = small_font.render(f"Čekajících: {waiting_customers}", True, BLACK)
            #     screen.blit(waiting_text, (20, 80))

    pygame.display.flip()

pygame.quit()
sys.exit()