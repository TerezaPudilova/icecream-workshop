import pygame
import sys

# Inicializace Pygame
pygame.init()

# Nastavení velikosti okna
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Obsluha Zmrzlinárny")

# FPS a časovač
clock = pygame.time.Clock()
FPS = 60

# Barvy
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Načtení fontu
font = pygame.font.SysFont("arial", 48)

# Definování tříd
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("icecream/assets/Staff/Waiter.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.midtop = (WIDTH // 2, 20)  # Nahoru doprostřed

    def update(self):
        pass


class Customer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("icecream/assets/Customers/Customer1FF.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (20, HEIGHT - 20)  # Levý dolní roh

    def update(self):
        pass

# Stav hry
STATE = "intro"  # intro -> menu -> hra

all_sprites = pygame.sprite.Group()
player = Player()
customer = Customer()


# Načasování pro přechod z intro do menu
intro_start_time = pygame.time.get_ticks()

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

    # Aktualizace obrazovky
    pygame.display.flip()

# Ukončení
pygame.quit()
sys.exit()
