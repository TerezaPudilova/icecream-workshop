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
DISPENSER_RECT = pygame.Rect(WIDTH - 180, HEIGHT - 220, 160, 200)

# FPS a časovač
clock = pygame.time.Clock()
FPS = 60

# Barvy
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Fonty
font = pygame.font.SysFont("arial", 48)
small_font = pygame.font.SysFont("arial", 16)

# Načtení obrázků
cone_img = pygame.image.load("icecream/assets/Icecream/kornout.png").convert_alpha()
scoop1_img = pygame.image.load("icecream/assets/Icecream/cokoladova.png").convert_alpha()
scoop2_img = pygame.image.load("icecream/assets/Icecream/smoulova.png").convert_alpha()

score = 0

class DraggableItem:
    def __init__(self, image, label, start_pos):
        self.image = pygame.transform.scale(image, (48, 48))
        self.label = label
        self.rect = self.image.get_rect(topleft=start_pos)
        self.dragging = False
        self.offset = (0, 0)
        self.placed = False

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    def handle_event(self, event):
        global score
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                mouse_x, mouse_y = event.pos
                self.offset = (self.rect.x - mouse_x, self.rect.y - mouse_y)

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

            drop_zone = pygame.Rect(ASSEMBLY_CENTER[0] - 30, ASSEMBLY_CENTER[1] - 100, 60, 120)
            if drop_zone.colliderect(self.rect) and not self.placed:
                self.rect.center = (ASSEMBLY_CENTER[0], ASSEMBLY_CENTER[1] - len(assembled_items) * 30)
                assembled_items.append(self)
                self.placed = True

            if self.placed and DISPENSER_RECT.collidepoint(self.rect.center):
                if assembled_items:
                    recipe = {"cone": None, "scoops": []}
                    for item in assembled_items:
                        if item.label == "cone":
                            recipe["cone"] = "klasický"
                        elif item.label == "scoop1":
                            recipe["scoops"].append("čokoláda")
                        elif item.label == "scoop2":
                            recipe["scoops"].append("šmoulová")

                    icecream = IceCream(assembled_items.copy(), recipe)
                    assembled_items.clear()
                    icecream.rect.center = DISPENSER_RECT.center
                    icecream_group.add(icecream)

                    if pygame.sprite.spritecollideany(icecream, dispenser_group):
                        if customer.order and icecream.check_with_order(customer.order):
                            print("✅ Objednávka správná!")
                            player.deliver_to(customer)
                            score += 1
                        else:
                            print("❌ Objednávka nesedí. Zkus to znovu.")

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

class Order:
    def __init__(self):
        self.cone = "klasický"
        self.scoops = random.sample(["čokoláda", "šmoulová"], random.randint(1, 2))

    def get_text(self):
        return f"{self.cone} kornout, {', '.join(self.scoops)}"

class IceCream(pygame.sprite.Sprite):
    def __init__(self, items, recipe):
        super().__init__()
        self.image = pygame.Surface((60, 120), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=ASSEMBLY_CENTER)
        self.recipe = recipe
        for i, item in enumerate(items):
            self.image.blit(item.image, (6, 100 - i * 30))

    def check_with_order(self, order):
        return self.recipe['cone'] == order.cone and sorted(self.recipe['scoops']) == sorted(order.scoops)

class Dispenser(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((160, 200), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(WIDTH - 180, HEIGHT - 220))

STATE = "intro"
dispenser = Dispenser()
dispenser_group = pygame.sprite.Group(dispenser)
icecream_group = pygame.sprite.Group()
drag_items = []
assembled_items = []
player = Player()
customer = Customer()
all_sprites = pygame.sprite.Group(player, customer)
intro_start_time = pygame.time.get_ticks()

# --- Hlavní smyčka ---
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if STATE == "menu":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    drag_items.clear()
                    cone_item = DraggableItem(cone_img, "cone", (WIDTH - 160 + 10, 60))
                    scoop1_item = DraggableItem(scoop1_img, "scoop1", (WIDTH - 160 + 10, 120))
                    scoop2_item = DraggableItem(scoop2_img, "scoop2", (WIDTH - 160 + 10, 180))
                    drag_items.extend([cone_item, scoop1_item, scoop2_item])
                    STATE = "playing"
        if STATE == "playing":
            for item in drag_items:
                item.handle_event(event)

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
        dispenser_group.draw(screen)

        draw_rect = pygame.Rect(WIDTH - 180, HEIGHT - 220, 160, 200)
        pygame.draw.rect(screen, (220, 255, 220), draw_rect)
        pygame.draw.rect(screen, (0, 120, 0), draw_rect, 2)
        dispenser_title = small_font.render("VÝDEJNÍ MÍSTO", True, (0, 100, 0))
        screen.blit(dispenser_title, (draw_rect.centerx - dispenser_title.get_width() // 2, draw_rect.top - 20))

        for item in assembled_items:
            item.draw(screen)

        for icecream in icecream_group:
            screen.blit(icecream.image, icecream.rect)

        panel_rect = pygame.Rect(WIDTH - 180, 20, 160, 200)
        pygame.draw.rect(screen, (230, 230, 230), panel_rect)
        pygame.draw.rect(screen, BLACK, panel_rect, 2)
        title = small_font.render("Tvoje zmrzlina", True, BLACK)
        screen.blit(title, (panel_rect.x + 10, panel_rect.y + 10))

        for i, item in enumerate(drag_items):
            if not item.placed:
                item.draw(screen)

        score_text = small_font.render(f"Skóre: {score}", True, BLACK)
        screen.blit(score_text, (20, 20))
        customer.draw_order(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()
