import pygame
import random
import math

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