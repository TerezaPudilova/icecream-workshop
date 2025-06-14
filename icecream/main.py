import pygame
import sys
import random

# Inicializace Pygame
pygame.init()

# Nastavení velikosti okna
WIDTH, HEIGHT = 800, 600
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

# Fonty
font = pygame.font.SysFont("arial", 48)
small_font = pygame.font.SysFont("arial", 16)
button_font = pygame.font.SysFont("arial", 20)

# Načtení obrázků
cone_img = pygame.image.load("icecream/assets/Icecream/kornout.png").convert_alpha()
scoop1_img = pygame.image.load("icecream/assets/Icecream/cokoladova.png").convert_alpha()
scoop2_img = pygame.image.load("icecream/assets/Icecream/smoulova.png").convert_alpha()

score = 0

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
        """Vrátí položku na původní pozici"""
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
                # Kontrola, zda je položka v oblasti sestavování
                assembly_zone = pygame.Rect(ASSEMBLY_CENTER[0] - 50, ASSEMBLY_CENTER[1] - 150, 100, 200)
                if assembly_zone.colliderect(self.rect):
                    # Umístění na správnou pozici v sestavě
                    self.rect.center = (ASSEMBLY_CENTER[0], ASSEMBLY_CENTER[1] - len(assembled_items) * 30)
                    assembled_items.append(self)
                    self.placed = True
                else:
                    # Pokud není v zóně, vrátí se na původní místo
                    self.reset_position()

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                mouse_x, mouse_y = event.pos
                self.rect.x = mouse_x + self.offset[0]
                self.rect.y = mouse_y + self.offset[1]

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("icecream/assets/Staff/Waiter.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.midtop = (WIDTH // 2, 20)
        self.delivering = False

    def update(self):
        if self.delivering:
            if self.rect.centerx > customer.rect.centerx + 40:
                self.rect.centerx -= 2
            elif self.rect.centerx < customer.rect.centerx - 40:
                self.rect.centerx += 2
            elif self.rect.centery < customer.rect.centery - 60:
                self.rect.centery += 2
            else:
                self.delivering = False
                print("Zmrzlina předána zákazníkovi!")

    def deliver_to(self, customer):
        self.delivering = True

class Customer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("icecream/assets/Customers/Customer1FF.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (20, HEIGHT - 20)
        self.order = None
        self.show_order = False
        self.font = pygame.font.SysFont("arial", 14)
        self.target_x = WIDTH // 2
        self.target_y = 160
        self.speed = 2
        self.phase = 1

    def update(self):
        if self.phase == 1:
            if self.rect.centerx < self.target_x:
                self.rect.centerx += self.speed
            else:
                self.phase = 2
        elif self.phase == 2:
            if self.rect.centery > self.target_y:
                self.rect.centery -= self.speed
            else:
                self.phase = 0

        if self.phase == 0 and not self.show_order:
            self.order = Order()
            self.show_order = True

    def draw_order(self, surface):
        if self.show_order and self.order:
            text = self.order.get_text()
            text_surface = self.font.render(text, True, BLACK)
            bubble_x = self.rect.centerx - text_surface.get_width() - 30
            bubble_y = self.rect.top - 50
            padding = 6
            bubble_rect = pygame.Rect(bubble_x, bubble_y, text_surface.get_width() + 2 * padding, text_surface.get_height() + 2 * padding)
            pygame.draw.rect(surface, WHITE, bubble_rect, border_radius=8)
            pygame.draw.rect(surface, BLACK, bubble_rect, 2, border_radius=8)
            surface.blit(text_surface, (bubble_x + padding, bubble_y + padding))

    def new_order(self):
        """Vytvoří novou objednávku"""
        self.order = Order()

class Order:
    def __init__(self):
        self.cone = "klasický"
        self.scoops = random.sample(["čokoláda", "šmoulová"], random.randint(1, 2))

    def get_text(self):
        return f"{self.cone} kornout, {', '.join(self.scoops)}"

def check_order_correctness():
    """Kontroluje, zda sestavená zmrzlina odpovídá objednávce"""
    if not customer.order or not assembled_items:
        return False
    
    # Sestavení receptu z položek
    recipe = {"cone": None, "scoops": []}
    for item in assembled_items:
        if item.label == "cone":
            recipe["cone"] = "klasický"
        elif item.label == "scoop1":
            recipe["scoops"].append("čokoláda")
        elif item.label == "scoop2":
            recipe["scoops"].append("šmoulová")
    
    # Kontrola správnosti
    return (recipe['cone'] == customer.order.cone and 
            sorted(recipe['scoops']) == sorted(customer.order.scoops))

def reset_assembly():
    """Vyčistí místo sestavování a vrátí ingredience"""
    global assembled_items
    for item in assembled_items:
        item.reset_position()
    assembled_items.clear()

def complete_order():
    """Dokončí objednávku a vytvoří novou"""
    global score
    
    if check_order_correctness():
        print("✅ Objednávka správná!")
        score += 1
        player.deliver_to(customer)
        reset_assembly()
        # Vytvoření nové objednávky po krátké pauze
        pygame.time.set_timer(pygame.USEREVENT + 1, 2000)  # 2 sekundy
    else:
        print("❌ Objednávka nesedí. Zkus to znovu.")

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
player = Player()
customer = Customer()
all_sprites = pygame.sprite.Group(player, customer)
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
            
        elif event.type == pygame.USEREVENT + 1:
            # Vytvoření nové objednávky
            customer.new_order()
            pygame.time.set_timer(pygame.USEREVENT + 1, 0)  # Zrušení časovače
            
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
        pygame.draw.rect(screen, (240, 240, 255), assembly_zone, border_radius=10)
        pygame.draw.rect(screen, (100, 100, 200), assembly_zone, 3, border_radius=10)
        
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
        screen.blit(score_text, (20, 20))
        
        # Vykreslení objednávky
        customer.draw_order(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()