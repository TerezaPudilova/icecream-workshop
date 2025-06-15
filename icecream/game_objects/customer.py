import pygame
from .order import Order


class Customer(pygame.sprite.Sprite):
    spacing = 60
    
    def __init__(self, customer_id, window_width=1200):
        super().__init__()
        try:
            # Použití helper funkce
            image_path = "assets/Customers/Customer1FF.png"
            self.image = pygame.image.load(image_path).convert_alpha()
        except pygame.error:
            print("Nepodařilo se načíst obrázek zákazníka, používám placeholder...")
            # Vytvoření placeholder zákazníka
            self.image = pygame.Surface((64, 96), pygame.SRCALPHA)
            # Hlava
            pygame.draw.circle(self.image, (255, 220, 177), (32, 20), 15)
            # Tělo
            pygame.draw.rect(self.image, (100, 100, 200), (20, 35, 24, 40))
            # Nohy
            pygame.draw.rect(self.image, (50, 50, 100), (24, 75, 6, 20))
            pygame.draw.rect(self.image, (50, 50, 100), (34, 75, 6, 20))
        
        self.rect = self.image.get_rect()
        self.window_width = window_width
        self.customer_id = customer_id
        self.order = Order()
        self.show_order = False
        self.font = pygame.font.SysFont("arial", 14)

        self.target_y = 100

        if customer_id == 0:
            self.rect.topleft = (-self.rect.width, self.target_y)
            self.target_x = self.window_width // 2 - 100
        else:
            self.rect.topleft = (-self.rect.width, self.target_y)
            if customer_id == 1:
                self.target_x = self.window_width // 2 - 100 - 3 * self.spacing
            elif customer_id >= 2:
                self.target_x = self.window_width // 2 - 100 - 3 * self.spacing - (customer_id - 1) * self.spacing

        self.speed = 4
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
                abs(self.rect.centery - self.target_y) < 3):
                self.arrived = True
                if self.customer_id == 0:
                    self.show_order = True

    def move_in_queue(self, new_position):
        self.customer_id = new_position
        self.target_y = 100

        if new_position == 0:
            self.target_x = self.window_width // 2 - 100
        elif new_position == 1:
            self.target_x = self.window_width // 2 - 100 - 200
        else:
            self.target_x = self.window_width // 2 - 100 - 200 - (new_position - 1) * 60

        if (abs(self.rect.centerx - self.target_x) > 3 or 
            abs(self.rect.centery - self.target_y) > 3):
            self.arrived = False
            self.show_order = False

    def draw_order(self, surface):
        if self.show_order and self.order and not self.served:
            order_font = pygame.font.SysFont("arial", 18)
            small_font = pygame.font.SysFont("arial", 16)
            
            text = self.order.get_text()
            text_surface = order_font.render(text, True, (0, 0, 0))
            bubble_x = self.window_width // 2 - 100 - text_surface.get_width() // 2
            bubble_y = 40
            padding = 12
            bubble_rect = pygame.Rect(bubble_x - padding, bubble_y - padding, 
                                      text_surface.get_width() + 2 * padding, 
                                      text_surface.get_height() + 2 * padding)
            pygame.draw.rect(surface, (255, 255, 0), bubble_rect, border_radius=10)
            pygame.draw.rect(surface, (0, 0, 0), bubble_rect, 3, border_radius=10)
            title_text = small_font.render("AKTUÁLNÍ OBJEDNÁVKA", True, (150, 0, 0))
            title_x = bubble_x + (bubble_rect.width - title_text.get_width()) // 2
            surface.blit(title_text, (title_x, bubble_y - padding - 25))
            surface.blit(text_surface, (bubble_x, bubble_y))

    def serve(self):
        self.served = True
        self.show_order = False
        self.kill()