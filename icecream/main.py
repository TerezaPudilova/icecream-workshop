import pygame
import sys
import random

# Inicializace Pygame
pygame.init()

# Nastavení velikosti okna
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Obsluha Zmrzlinárny")

# 💡 Umísti sem:
ASSEMBLY_CENTER = (WIDTH // 2, HEIGHT // 2 + 100)

DISPENSER_RECT = pygame.Rect(WIDTH - 180, HEIGHT - 220, 160, 200) # x, y, šířka, výška

# FPS a časovač
clock = pygame.time.Clock()
FPS = 60

# Barvy
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Načtení fontu
font = pygame.font.SysFont("arial", 48)

# Ice cream assets
cone_img = pygame.image.load("icecream/assets/Icecream/kornout.png").convert_alpha()
scoop1_img = pygame.image.load("icecream/assets/Icecream/cokoladova.png").convert_alpha()
scoop2_img = pygame.image.load("icecream/assets/Icecream/smoulova.png").convert_alpha()

# Definování tříd

class DraggableItem:
    def __init__(self, image, start_pos):
        self.image = pygame.transform.scale(image, (48, 48))
        self.rect = self.image.get_rect(topleft=start_pos)
        self.dragging = False
        self.offset = (0, 0)
        self.placed = False

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                mouse_x, mouse_y = event.pos
                self.offset = (self.rect.x - mouse_x, self.rect.y - mouse_y)

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

            # Kontrola, zda byl upuštěn v oblasti zmrzliny
            drop_zone = pygame.Rect(ASSEMBLY_CENTER[0] - 30, ASSEMBLY_CENTER[1] - 100, 60, 120)
            if drop_zone.colliderect(self.rect) and not self.placed:
                self.rect.center = (ASSEMBLY_CENTER[0], ASSEMBLY_CENTER[1] - len(assembled_items) * 30)
                assembled_items.append(self)
                self.placed = True

            # 💡 Nová část: Pokud byl předmět položen a nyní přesunut do výdejního místa
            if self.placed and DISPENSER_RECT.collidepoint(self.rect.center):
                print("Zmrzlina připravena k výdeji!")
                player.deliver_to(customer)


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
        self.rect.midtop = (WIDTH // 2, 20)  # Nahoru doprostřed
        self.delivering = False

    def update(self):
        if self.delivering:
            # Pohyb směrem k zákazníkovi
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
        self.rect.bottomleft = (20, HEIGHT - 20)  # Levý dolní roh
        self.order = None  # objednávka se vytvoří až po zastavení
        self.show_order = False
        self.font = pygame.font.SysFont("arial", 14)



        # Cílové pozice
        self.target_x = WIDTH // 2
        self.target_y = 160  # těsně před obsluhu
        self.speed = 2
        self.phase = 1  # 1 = doprava, 2 = nahoru, 0 = stojí

    def update(self):
        if self.phase == 1:
            # Pohyb doprava
            if self.rect.centerx < self.target_x:
                self.rect.centerx += self.speed
            else:
                self.phase = 2  # Přechod do fáze 2 (nahoru)

        elif self.phase == 2:
            # Pohyb nahoru
            if self.rect.centery > self.target_y:
                self.rect.centery -= self.speed
            else:
                self.phase = 0  # Zastaví se

        if self.phase == 0 and not self.show_order:
            self.order = Order()
            self.show_order = True

    def draw_order(self, surface):
        if self.show_order and self.order:
            text = self.order.get_text()
            text_surface = self.font.render(text, True, (0, 0, 0))

            # Menší a lehce vlevo
            bubble_x = self.rect.centerx - text_surface.get_width() - 30
            bubble_y = self.rect.top - 50

            padding = 6  # zmenšený vnitřní okraj
            bubble_width = text_surface.get_width() + padding * 2
            bubble_height = text_surface.get_height() + padding * 2

            # Bublina s oblými rohy
            bubble_rect = pygame.Rect(bubble_x, bubble_y, bubble_width, bubble_height)
            pygame.draw.rect(surface, (255, 255, 255), bubble_rect, border_radius=8)
            pygame.draw.rect(surface, (0, 0, 0), bubble_rect, width=2, border_radius=8)

            # Zobáček menší
            point1 = (bubble_rect.right - 20, bubble_rect.bottom)
            point2 = (point1[0] + 10, point1[1] + 10)
            point3 = (point1[0] - 10, point1[1])
            pygame.draw.polygon(surface, (255, 255, 255), [point1, point2, point3])
            pygame.draw.polygon(surface, (0, 0, 0), [point1, point2, point3], 2)

            # Text
            surface.blit(text_surface, (bubble_x + padding, bubble_y + padding))

        

class Order:
    def __init__(self):
        self.cones = ["klasický", "vaflový"]
        self.flavors = ["jahoda", "čokoláda", "vanilka"]
        self.toppings = ["karamel", "čokoládová poleva"]

        # Vygeneruj objednávku
        self.cone = random.choice(self.cones)
        self.scoops = random.sample(self.flavors, random.randint(1, 3))
        self.topping = random.choice(self.toppings + [None])  # může být bez polevy

    def get_text(self):
        scoops_text = ", ".join(self.scoops)
        topping_text = f", s polevou: {self.topping}" if self.topping else ""
        return f"{self.cone} kornout, {scoops_text}{topping_text}"               

# Stav hry
STATE = "intro"  # intro -> menu -> hra

# Položky v menu, které lze přetahovat
draggable_items = []
assembled_items = []

all_sprites = pygame.sprite.Group()
player = Player()
customer = Customer()


# Načasování pro přechod z intro do menu
intro_start_time = pygame.time.get_ticks()

def draw_icecream_preview(surface):
    # --- Rozměry a pozice menu ---
    panel_width = 160
    panel_height = 200
    panel_x = WIDTH - panel_width - 20
    panel_y = 20

    # --- Vykresli panel pozadí ---
    panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
    pygame.draw.rect(surface, (230, 230, 230), panel_rect)  # světle šedé pozadí
    pygame.draw.rect(surface, (0, 0, 0), panel_rect, 2)      # černý okraj

    # --- Popisek ---
    font = pygame.font.SysFont("arial", 20)
    title = font.render("Tvoje zmrzlina", True, (0, 0, 0))
    surface.blit(title, (panel_x + 10, panel_y + 10))

    # --- Vykresli jednotlivé položky s rámečky ---
    item_padding = 10
    item_size = 48
    start_y = panel_y + 40

    # Kornout
    cone_rect = pygame.Rect(panel_x + item_padding, start_y, item_size, item_size)
    pygame.draw.rect(surface, (255, 255, 255), cone_rect)
    pygame.draw.rect(surface, (0, 0, 0), cone_rect, 1)
    surface.blit(pygame.transform.scale(cone_img, (item_size, item_size)), cone_rect)

    # Kopeček 1
    scoop1_rect = pygame.Rect(panel_x + item_padding, start_y + item_size + 10, item_size, item_size)
    pygame.draw.rect(surface, (255, 255, 255), scoop1_rect)
    pygame.draw.rect(surface, (0, 0, 0), scoop1_rect, 1)
    surface.blit(pygame.transform.scale(scoop1_img, (item_size, item_size)), scoop1_rect)

    # Kopeček 2
    scoop2_rect = pygame.Rect(panel_x + item_padding, start_y + 2 * (item_size + 10), item_size, item_size)
    pygame.draw.rect(surface, (255, 255, 255), scoop2_rect)
    pygame.draw.rect(surface, (0, 0, 0), scoop2_rect, 1)
    surface.blit(pygame.transform.scale(scoop2_img, (item_size, item_size)), scoop2_rect)

def draw_dispenser_area(surface):
    panel_rect = DISPENSER_RECT
    pygame.draw.rect(surface, (220, 255, 220), panel_rect)  # světle zelené pozadí
    pygame.draw.rect(surface, (0, 120, 0), panel_rect, 2)    # tmavě zelený okraj

    font_small = pygame.font.SysFont("arial", 16)
    title = font_small.render("VÝDEJNÍ MÍSTO", True, (0, 100, 0))
    surface.blit(title, (panel_rect.centerx - title.get_width() // 2, panel_rect.top - 20))



# --------------------- HLAVNÍ SMYČKA ---------------------

running = True

while running:
    clock.tick(FPS)

    # Zpracování událostí
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if STATE == "menu":
             if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    all_sprites.add(player, customer)
                    STATE = "playing"

                    # Vytvoření přetahovatelných položek
                    draggable_items.clear()  # pokud by se vracel do menu a hrál znovu
                    cone_item = DraggableItem(cone_img, (WIDTH - 160 + 10, 60))
                    scoop1_item = DraggableItem(scoop1_img, (WIDTH - 160 + 10, 120))
                    scoop2_item = DraggableItem(scoop2_img, (WIDTH - 160 + 10, 180))
                    draggable_items.extend([cone_item, scoop1_item, scoop2_item])
                    pass

        if STATE == "playing":
            for item in draggable_items:
                item.handle_event(event)

        pygame.draw.rect(screen, (200, 200, 255), (ASSEMBLY_CENTER[0] - 30, ASSEMBLY_CENTER[1] - 100, 60, 120), 2)

        # Výdejní místo
        pygame.draw.rect(screen, (200, 255, 200), DISPENSER_RECT)
        pygame.draw.rect(screen, (0, 100, 0), DISPENSER_RECT, 2)
        disp_text = pygame.font.SysFont("arial", 16).render("VÝDEJ", True, (0, 100, 0))
        screen.blit(disp_text, (DISPENSER_RECT.centerx - disp_text.get_width() // 2, DISPENSER_RECT.centery - 8))
                     

    # Vymazání obrazovky
    screen.fill(WHITE)

    # --- OBRAZOVKY DLE STAVU ---
    if STATE == "intro":
        text = font.render("Vítejte v Zmrzlinárně!", True, BLACK)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 50))

        # Přechod do menu po 3 sekundách
        if pygame.time.get_ticks() - intro_start_time > 3000:
            STATE = "menu"

    elif STATE == "menu":
        text = font.render("MENU", True, BLACK)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 100))

        button_text = font.render("HRÁT", True, BLACK)
        button_rect = button_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(button_text, button_rect)

        # Zpracování kliknutí na tlačítko HRÁT
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                STATE = "game"

    elif STATE == "game":
        text = font.render("HRA ZAČALA", True, BLACK)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 50))

    elif STATE == "playing":
        all_sprites.update()
        all_sprites.draw(screen)    
        draw_icecream_preview(screen)
        draw_dispenser_area(screen)

        # Vykresli složenou zmrzlinu podle pořadí
        for item in assembled_items:
            item.draw(screen)  # první = spodní, poslední = horní

        # Vykresli přetahované položky (ty, které ještě nejsou položené)
        for item in draggable_items:
            if not item.placed:
                item.draw(screen)

        customer.draw_order(screen)

    # Aktualizace obrazovky
    pygame.display.flip()

# Ukončení
pygame.quit()
sys.exit()
